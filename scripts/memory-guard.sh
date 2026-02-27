#!/usr/bin/env bash

# memory-guard.sh — Backs up MEMORY.md BEFORE it gets overwritten
# Compares checksum, saves old version if changed
# Run via cron every 5 min on each server
# Usage: ./memory-guard.sh

WORKSPACE="/data/openclaw/workspace"
MEMORY="$WORKSPACE/MEMORY.md"
BACKUP_DIR="$WORKSPACE/.memory-backups"
CHECKSUM_FILE="$BACKUP_DIR/.last-checksum"
MAX_BACKUPS=30

[ ! -f "$MEMORY" ] && exit 0

mkdir -p "$BACKUP_DIR"

# Current checksum
CURRENT=$(md5sum "$MEMORY" | awk '{print $1}')

# Previous checksum
PREVIOUS=""
[ -f "$CHECKSUM_FILE" ] && PREVIOUS=$(cat "$CHECKSUM_FILE")

# If unchanged, nothing to do
[ "$CURRENT" = "$PREVIOUS" ] && exit 0

# Changed! Save the CURRENT version (which is the new one)
# But we want the OLD one. We can't get the old content anymore
# unless we keep a shadow copy. So we maintain a shadow.
SHADOW="$BACKUP_DIR/.shadow-MEMORY.md"

if [ -f "$SHADOW" ]; then
    # Shadow has the PREVIOUS content — back it up
    TS=$(date +%Y%m%d-%H%M%S)
    cp "$SHADOW" "$BACKUP_DIR/MEMORY-${TS}.md"
    echo "[memory-guard] Backed up previous MEMORY.md as MEMORY-${TS}.md"
fi

# Update shadow with current content
cp "$MEMORY" "$SHADOW"

# Update checksum
echo "$CURRENT" > "$CHECKSUM_FILE"

# Prune old backups, keep last N
cd "$BACKUP_DIR"
ls -t MEMORY-*.md 2>/dev/null | tail -n +$((MAX_BACKUPS + 1)) | xargs rm -f 2>/dev/null

exit 0
