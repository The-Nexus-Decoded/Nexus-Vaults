#!/bin/bash
# Manual Deployment Rune (rsync + SSH bypass)
TARGET_HOST="[REDACTED_TS_IP]"
TARGET_USER="olawal"
TARGET_DIR="/data/openclaw/workspace/Pryan-Fire"

echo "🗡️ Initiating rsync strike to ${TARGET_HOST}..."
rsync -avz --exclude 'node_modules' --exclude '.git' ./ ${TARGET_USER}@${TARGET_HOST}:${TARGET_DIR}
