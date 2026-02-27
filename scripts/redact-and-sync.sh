#!/usr/bin/env bash

# redact-and-sync.sh — Fleet workspace backup with redaction
# Syncs all 3 agents' workspaces to Nexus-Vaults repo
# Usage: ./redact-and-sync.sh [--dry-run]

set -e

REPO_DIR="/data/repos/Nexus-Vaults"
KEYS_DIR="/data/openclaw/keys"

# Rsync exclusions — skip large data, caches, binaries, backups
EXCLUDE=(
  --exclude 'node_modules/'
  --exclude 'venv/'
  --exclude '.venv/'
  --exclude '.git/'
  --exclude '__pycache__/'
  --exclude '*.db'
  --exclude '*.sqlite'
  --exclude '*.pyc'
  --exclude '*.jsonl'
  --exclude 'owner_intelligence/'
  --exclude 'nexus-vaults-restore/'
  --exclude 'OWNER_PROFILE_RAW.md'
  --exclude 'full_documents_scan_output.txt'
  --exclude 'project_scan_output.txt'
  --exclude '*.bak*'
  --exclude '*.pre-sync*'
  --exclude 'staging_windows_docs/'
  --exclude 'H:\*'
  --exclude 'document_index.db'
  --exclude 'testvenv/'
  --exclude 'site-packages/'
)

# Server definitions: name:source_type:source_path
SERVERS=(
  "ola-claw-main:local:/data/openclaw/workspace"
  "ola-claw-trade:ssh:[REDACTED_TS_IP]:/data/openclaw/workspace"
  "ola-claw-dev:ssh:[REDACTED_TS_IP]:/data/openclaw/workspace"
)

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1 && echo "[INFO] DRY RUN mode"

redact_dir() {
    local dir="$1"
    [ ! -d "$dir" ] && return

    # Only redact text files under 500KB
    find "$dir" -type f -size -500k \( -name "*.md" -o -name "*.txt" -o -name "*.sh" -o -name "*.py" -o -name "*.js" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" -o -name "*.env" -o -name "*.toml" -o -name "*.cfg" -o -name "*.conf" \) -print0 | while IFS= read -r -d '' f; do
        sed -i \
            -e 's/github_pat_[a-zA-Z0-9_]*/[REDACTED_GH_PAT]/g' \
            -e 's/sk-[a-zA-Z0-9_-]*/[REDACTED_API_KEY]/g' \
            -e 's/AIzaSy[a-zA-Z0-9_-]*/[REDACTED_GOOGLE_KEY]/g' \
            -e 's/Bearer [a-zA-Z0-9_.=-]*/Bearer [REDACTED_TOKEN]/g' \
            -e 's/100\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/[REDACTED_TS_IP]/g' \
            -e 's/[a-zA-Z0-9_-]\{24\}\.[a-zA-Z0-9_-]\{6\}\.[a-zA-Z0-9_-]\{27,\}/[REDACTED_DISCORD_TOKEN]/g' \
            "$f" 2>/dev/null || true
    done

    # Redact dynamic keys if available
    if [ -d "$KEYS_DIR" ]; then
        find "$KEYS_DIR" -type f 2>/dev/null | while read keyfile; do
            while IFS= read -r keyval; do
                [ -z "$keyval" ] && continue
                safe_val=$(printf '%s\n' "$keyval" | sed -e 's/[][\/$*.^]/\\&/g')
                find "$dir" -type f -size -500k -print0 | xargs -0 sed -i "s#${safe_val}#[REDACTED_KEY]#g" 2>/dev/null || true
            done < "$keyfile"
        done
    fi
}

sync_server() {
    local name="${1%%:*}"
    local rest="${1#*:}"
    local type="${rest%%:*}"
    local path="${rest#*:}"
    local staging="/tmp/nexus-staging-${name}-$$"
    local agent_dir="$REPO_DIR/$name"

    echo "[INFO] Syncing $name..."
    mkdir -p "$staging"

    if [ "$type" = "local" ]; then
        rsync -a "${EXCLUDE[@]}" "$path/" "$staging/" 2>/dev/null || true
    elif [ "$type" = "ssh" ]; then
        local remote_ip="${path%%:*}"
        local remote_path="${path#*:}"
        rsync -a -e 'ssh -o ConnectTimeout=10 -o BatchMode=yes' "${EXCLUDE[@]}" "openclaw@${remote_ip}:${remote_path}/" "$staging/" 2>/dev/null || {
            echo "[WARN] Failed to rsync from $name ($remote_ip). Skipping."
            rm -rf "$staging"
            return
        }
    fi

    echo "[INFO] Redacting secrets for $name..."
    redact_dir "$staging"

    echo "[INFO] Updating repo: $agent_dir"
    mkdir -p "$agent_dir"
    rsync -a --delete "$staging/" "$agent_dir/"
    rm -rf "$staging"
}

# Sync all servers
for server in "${SERVERS[@]}"; do
    sync_server "$server"
done

cd "$REPO_DIR"
git add -A

if git diff --cached --quiet; then
    echo "[INFO] No changes to commit."
    exit 0
fi

# Quick secret scan on diff
if git diff --cached -- . ':(exclude)scripts/' | grep -qE 'AIzaSy[a-zA-Z0-9_-]{20,}|github_pat_[a-zA-Z0-9_]{20,}|sk-or-v1-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}' 2>/dev/null; then
    echo "[ERROR] Potential un-redacted secrets in diff! Aborting."
    git reset HEAD . >/dev/null 2>&1
    exit 1
fi

if [ $DRY_RUN -eq 0 ]; then
    git commit -m "auto: fleet workspace sync $(date '+%Y-%m-%d %H:%M')"
    git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "[WARN] Push failed — run manually"
    echo "[INFO] Done. All 3 workspaces synced and pushed."
else
    echo "[INFO] Dry run complete. Changes staged but not committed."
    git reset HEAD . >/dev/null 2>&1
fi
