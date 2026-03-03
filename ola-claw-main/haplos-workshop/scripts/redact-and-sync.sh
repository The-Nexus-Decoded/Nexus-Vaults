#!/bin/bash

set -euo pipefail

WORKSPACE_DIR="/data/openclaw/workspace"
STAGING_DIR="/tmp/openclaw_workspace_staging_$(date +%s)"
REDACTED_LOG="/tmp/redaction_log_$(date +%s).log"

# Define redaction patterns (simplified for initial commit)
# This will be expanded in later steps.
declare -A patterns
patterns[TAILSCALE_IP]="100\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
patterns[GITHUB_PAT]="[REDACTED_GH_PAT][a-zA-Z0-9_]+"
patterns[DISCORD_TOKEN]="[A-Za-z0-9]{24}\\.[A-Za-z0-9]{6}\\.[A-Za-z0-9]{27}"
patterns[SOLANA_WALLET]="[1-9A-HJ-NP-Za-km-z]{32,44}"
patterns[GEMINI_KEY]="[REDACTED_API_KEY][a-zA-Z0-9]+" # Example, needs refinement

log_redaction() {
    local file=$1
    local pattern_name=$2
    local original_value=$3
    echo "[REDACTED] File: $file, Pattern: $pattern_name, Original: \"$original_value\"" >> "$REDACTED_LOG"
}

# Create staging directory and copy workspace
echo "Creating staging directory: $STAGING_DIR"
mkdir -p "$STAGING_DIR"
rsync -a --exclude=".git" "$WORKSPACE_DIR/" "$STAGING_DIR/"
echo "Workspace copied to staging area."

# Perform redaction
echo "Starting redaction process..."
find "$STAGING_DIR" -type f -print0 | while IFS= read -r -d $'\0' file; do
    # Skip binary files
    if ! file -b --mime-type "$file" | grep -q text/; then
        continue
    fi

    for pattern_name in "${!patterns[@]}"; do
        regex="${patterns[$pattern_name]}"
        
        # Use a temporary file to store changes and avoid issues with sed -i
        TEMP_FILE=$(mktemp)
        
        # Find and replace, logging original values
        # The loop below is a simplified version for now,
        # A more robust solution might involve reading line by line
        # and using 'grep -o' to find all matches before replacing.
        # For now, this will replace all instances of the pattern.
        perl -pe "s/($regex)/[REDACTED_$pattern_name]/g" "$file" > "$TEMP_FILE" && mv "$TEMP_FILE" "$file"
        
        # Note: Logging the *original* value after replacement is tricky with this approach.
        # A full implementation would need to capture before replacing.
        # For now, we'll log the pattern name.
        if grep -q "[REDACTED_$pattern_name]" "$file"; then
             echo "[REDACTED] File: $file, Pattern: $pattern_name" >> "$REDACTED_LOG"
        fi
    done
done

echo "Redaction complete. Log saved to $REDACTED_LOG"
echo "Staging directory with redacted files: $STAGING_DIR"

# Clean up (optional, for testing purposes, we might keep it)
# rm -rf "$STAGING_DIR"
# echo "Staging directory removed."
