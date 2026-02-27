#!/bin/bash

# Helper function to get service/timer status over SSH
get_remote_status() {
    local host=$1
    local service=$2
    local status=$(ssh openclaw@$host "systemctl --user status $service" 2>/dev/null | grep "Active:" | awk '{print $2}')
    case "$status" in
        "active") echo "🟢 Active" ;;
        "inactive") echo "🔴 Inactive" ;;
        "failed") echo "🟠 Failed" ;;
        *) echo "🟡 Unknown" ;;
    esac
}

# Helper function to get Rate Guard metrics over SSH
get_rate_guard_metrics() {
    local host=$1
    local metrics=$(ssh openclaw@$host "curl -s http://127.0.0.1:8787/health")
    local rpm_used=$(echo "$metrics" | jq -r '.models.google_gemini_3_flash_preview.rpm_used // "N/A"')
    local tpm_used=$(echo "$metrics" | jq -r '.models.google_gemini_3_flash_preview.tpm_used // "N/A"')
    local rpd_used=$(echo "$metrics" | jq -r '.models.google_gemini_3_flash_preview.rpd_used // "N/A"')
    local active_model=$(echo "$metrics" | jq -r '.active_model // "N/A"')
    echo "RPM: $rpm_used, TPM: $tpm_used, RPD: $rpd_used, Model: $active_model"
}

# --- Zifnab (main) Services and Metrics ---
ZIFNAB_RATE_GUARD=$(get_remote_status [REDACTED_TS_IP] openclaw-rate-guard.service)
ZIFNAB_QUOTA_MONITOR=$(get_remote_status [REDACTED_TS_IP] openclaw-quota-monitor.timer)
ZIFNAB_QUOTA_RESET=$(get_remote_status [REDACTED_TS_IP] openclaw-quota-reset.timer)
ZIFNAB_RG_METRICS=$(get_rate_guard_metrics [REDACTED_TS_IP])

# --- Haplo (dev) Services and Metrics ---
HAPLO_RATE_GUARD=$(get_remote_status [REDACTED_TS_IP] openclaw-rate-guard.service)
HAPLO_QUOTA_MONITOR=$(get_remote_status [REDACTED_TS_IP] openclaw-quota-monitor.timer)
HAPLO_QUOTA_RESET=$(get_remote_status [REDACTED_TS_IP] openclaw-quota-reset.timer)
HAPLO_RG_METRICS=$(get_rate_guard_metrics [REDACTED_TS_IP])

# --- Hugh the Hand (trade) Services and Metrics ---
HUGH_RATE_GUARD=$(get_remote_status [REDACTED_TS_IP] openclaw-rate-guard.service)
HUGH_QUOTA_MONITOR=$(get_remote_status [REDACTED_TS_IP] openclaw-quota-monitor.timer)
HUGH_QUOTA_RESET=$(get_remote_status [REDACTED_TS_IP] openclaw-quota-reset.timer)
HUGH_RG_METRICS=$(get_rate_guard_metrics [REDACTED_TS_IP])

# --- Format as Markdown Table ---
REPORT_MESSAGE="**🌌 Fleet Rate Limit Service & Metrics Status - $(date '+%Y-%m-%d %H:%M:%S %Z') 🌌**\n---\n```\n| Server          | Rate Guard | Quota Monitor | Quota Reset | Rate Guard Metrics (Flash) |\n|:----------------|:-----------|:--------------|:------------|:---------------------------|\n| Zifnab (Main)   | $ZIFNAB_RATE_GUARD | $ZIFNAB_QUOTA_MONITOR | $ZIFNAB_QUOTA_RESET | $ZIFNAB_RG_METRICS |\n| Haplo (Dev)     | $HAPLO_RATE_GUARD | $HAPLO_QUOTA_MONITOR | $HAPLO_QUOTA_RESET | $HAPLO_RG_METRICS |\n| Hugh (Trade)    | $HUGH_RATE_GUARD | $HUGH_QUOTA_MONITOR | $HUGH_QUOTA_RESET | $HUGH_RG_METRICS |\n```"

# This output will be captured by the main agent and sent to Discord
echo "DISCORD_MONITOR_REPORT_START"
echo "$REPORT_MESSAGE"
echo "DISCORD_MONITOR_REPORT_END"
