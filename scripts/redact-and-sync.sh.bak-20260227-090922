#!/usr/bin/env bash

# redact-and-sync.sh
# Copies the OpenClaw workspace, redacts secrets, and prepares it for commit.
# Usage: ./redact-and-sync.sh [--dry-run]

set -e

SOURCE_DIR="/data/openclaw/workspace"
STAGING_DIR="/tmp/workspace-staging-$$"
REPO_DIR="/data/repos/Nexus-Vaults"
AGENT_DIR="$REPO_DIR/ola-claw-dev" # My workspace directory in the repo
KEYS_DIR="/data/openclaw/keys"

DRY_RUN=0
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=1
    echo "[INFO] Running in DRY RUN mode. No commits will be made."
fi

echo "[INFO] Copying workspace to staging: $STAGING_DIR"
mkdir -p "$STAGING_DIR"

# Copy safely ignoring large directories
rsync -av --exclude 'memory/' --exclude 'workflows/' --exclude 'node_modules/' --exclude 'venv/' --exclude '.venv/' --exclude '.git/' "$SOURCE_DIR/" "$STAGING_DIR/"
[ -d "$SOURCE_DIR/memory" ] && rsync -av "$SOURCE_DIR/memory/" "$STAGING_DIR/memory/"
[ -d "$SOURCE_DIR/workflows" ] && rsync -av "$SOURCE_DIR/workflows/" "$STAGING_DIR/workflows/"

echo "[INFO] Redacting secrets..."
replace() {
    local pattern="$1"
    local replacement="$2"
    # Using # as delimiter to avoid issues with standard keys, avoiding | just in case
    find "$STAGING_DIR" -type f -exec sed -i "s#$pattern#$replacement#g" {} +
}

replace 'github_pat_[a-zA-Z0-9_]*' '[REDACTED_GH_PAT]'
replace 'sk-[a-zA-Z0-9_]*' '[REDACTED_API_KEY]'
replace 'BSA[a-zA-Z0-9_]*' '[REDACTED_BSA_TOKEN]'
replace 'Bearer [a-zA-Z0-9_\.\-]*' 'Bearer [REDACTED_TOKEN]'
replace '100\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' '[REDACTED_IP]'
replace '[a-zA-Z0-9_-]\{24\}\.[a-zA-Z0-9_-]\{6\}\.[a-zA-Z0-9_-]\{27\}' '[REDACTED_DISCORD_TOKEN]'
replace '[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}' '[REDACTED_EMAIL]'
replace '\b[0-9]\{3\}-[0-9]\{3\}-[0-9]\{4\}\b' '[REDACTED_PHONE]'

if [ -d "$KEYS_DIR" ]; then
    echo "[INFO] Redacting dynamic keys from $KEYS_DIR"
    find "$KEYS_DIR" -type f | while read keyfile; do
        while read -r keyval; do
            if [ -n "$keyval" ]; then
                # Escape # and special chars roughly
                safe_val=$(printf '%s\n' "$keyval" | sed -e 's/[]\/$*.^[]/\\&/g' -e 's/#/\\#/g')
                replace "$safe_val" "[REDACTED_DYNAMIC_KEY]"
            fi
        done < "$keyfile"
    done
fi

echo "[INFO] Syncing to local repo: $AGENT_DIR"
mkdir -p "$AGENT_DIR"
rsync -a --delete "$STAGING_DIR/" "$AGENT_DIR/"

cd "$REPO_DIR"

echo "[INFO] Checking diff for potential missed secrets..."
git add "$AGENT_DIR"
git diff --cached > /tmp/workspace-diff.patch

if grep -qE 'password|secret|token|key|private' /tmp/workspace-diff.patch; then
    echo "[WARNING] Potential secrets found in the diff! Review /tmp/workspace-diff.patch"
    grep -E 'password|secret|token|key|private' /tmp/workspace-diff.patch | head -n 10
fi

if [ $DRY_RUN -eq 0 ]; then
    echo "[INFO] Committing and pushing..."
    git commit -m "chore(sync): update workspace for ola-claw-dev [redacted]" || echo "[INFO] No changes to commit"
    echo "[INFO] Use 'git push' to sync to remote."
else
    echo "[INFO] Dry run complete. Redacted files are in $AGENT_DIR."
    git reset HEAD "$AGENT_DIR" >/dev/null 2>&1
fi

rm -rf "$STAGING_DIR"
