#!/bin/bash

LOCAL_OUTPUT_LOG="/data/openclaw/workspace/owner_intelligence/windows_script_output.txt"
LOCAL_BATCH_LOG="/data/openclaw/workspace/owner_intelligence/windows_batch_copy.log"
REMOTE_OUTPUT_LOG="C:\tmp\windows_batch_script_output.txt"
REMOTE_BATCH_LOG="C:\tmp\windows_batch_copy.log"
REMOTE_HOST="olawal@[REDACTED_TS_IP]"

# Retrieve the Windows script output log
scp -q "$REMOTE_HOST:$REMOTE_OUTPUT_LOG" "$LOCAL_OUTPUT_LOG"

# Retrieve the verbose batch copy log
scp -q "$REMOTE_HOST:$REMOTE_BATCH_LOG" "$LOCAL_BATCH_LOG"

# Process the output log for Discord reports
REPORT_START_MARKER="OPENCLAW_DISCORD_REPORT_START"
REPORT_END_MARKER="OPENCLAW_DISCORD_REPORT_END"

# Read the local output log, look for markers, and extract message
# This assumes only one report per log check, or will take the last one
REPORT_MESSAGE=$(cat "$LOCAL_OUTPUT_LOG" | sed -n "/$REPORT_START_MARKER/,/$REPORT_END_MARKER/{ /$REPORT_START_MARKER/!{ /$REPORT_END_MARKER/!p } }" | tr -d '\r')

if [ -n "$REPORT_MESSAGE" ]; then
    # Send to Discord via the main agent's message tool
    echo "DISCORD_REPORT: $REPORT_MESSAGE"
    
    # Clear the remote output log after successful processing to avoid reprocessing old messages
    ssh "$REMOTE_HOST" "powershell -Command \"Set-Content -Path 'C:\\tmp\\windows_batch_script_output.txt' -Value \'\'\""
fi

# Optional: process the verbose batch log for errors if needed
# For now, we only focus on the Discord reports from the output log

