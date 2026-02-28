#!/bin/bash

# This script is a template for a git pre-commit hook.
# To activate it, copy it to .git/hooks/pre-commit in your repository:
# cp /data/openclaw/workspace/haplos-workshop/scripts/pre-commit-template.sh .git/hooks/pre-commit
# chmod +x .git/hooks/pre-commit

set -euo pipefail

# Define redaction patterns (must match those in redact-and-sync.sh)
declare -A patterns
patterns[TAILSCALE_IP]="100\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
patterns[GITHUB_PAT]="[REDACTED_GH_PAT][a-zA-Z0-9_]+"
patterns[DISCORD_TOKEN]="[A-Za-z0-9]{24}\\.[A-Za-z0-9]{6}\\.[A-Za-z0-9]{27}"
patterns[SOLANA_WALLET]="[1-9A-HJ-NP-Za-km-z]{32,44}"
patterns[GEMINI_KEY]="[REDACTED_API_KEY][a-zA-Z0-9]+"

SECRETS_FOUND=0

# Check staged files for secrets
echo "Running pre-commit hook: Checking for secrets..."

# Iterate over staged files
git diff --cached --name-only --diff-filter=ACM | while read -r file;
do
    # Skip binary files
    if ! file -b --mime-type "$file" | grep -q text/; then
        continue
    fi

    # Check for patterns in the file content
    for pattern_name in "${!patterns[@]}"; do
        regex="${patterns[$pattern_name]}"
        if grep -P -q "$regex" "$file"; then
            echo "⛔️ WARNING: Potential $pattern_name found in $file."
            SECRETS_FOUND=1
        fi
    done
done

if [ "$SECRETS_FOUND" -eq 1 ]; then
    echo "

⛔️ COMMIT BLOCKED: Secrets detected in staged files.
    Please redact these sensitive values before committing."
    exit 1
else
    echo "✅ No obvious secrets found in staged files."
fi
