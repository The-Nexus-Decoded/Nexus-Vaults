#!/bin/bash
# Fleet Status Monitor — services + rate guard summary per server
# Cron needs these for systemctl --user
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
# Posts to #jarvis via Discord bot API, runs every 15m via crontab on Zifnab
# Uses same local/ssh pattern as rate-guard-monitor.sh

JARVIS_CHANNEL="1475082997027049584"
DISCORD_BOT_TOKEN=$(python3 -c "import json; c=json.load(open('/home/openclaw/.openclaw/openclaw.json')); print(c['channels']['discord']['token'])" 2>/dev/null)
LOG="/data/openclaw/logs/fleet-status-monitor.log"
PARSER="/data/openclaw/workspace/fleet_parse.py"

SERVERS="zifnab:local haplo:ssh:[REDACTED_TS_IP] hugh:ssh:[REDACTED_TS_IP]"

timestamp=$(date '+%H:%M %Z')
report=""

for entry in $SERVERS; do
  name="${entry%%:*}"
  method="${entry#*:}"

  if [ "$method" = "local" ]; then
    gw=$(systemctl --user is-active openclaw-gateway.service 2>/dev/null)
    rg=$(systemctl --user is-active openclaw-rate-guard.service 2>/dev/null)
    health=$(curl -s --connect-timeout 5 "http://127.0.0.1:8787/health" 2>/dev/null)
  else
    remote_ip="${method#ssh:}"
    gw=$(ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "openclaw@${remote_ip}" \
      'systemctl --user is-active openclaw-gateway.service' 2>/dev/null)
    rg=$(ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "openclaw@${remote_ip}" \
      'systemctl --user is-active openclaw-rate-guard.service' 2>/dev/null)
    health=$(ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "openclaw@${remote_ip}" \
      'curl -s --connect-timeout 5 http://127.0.0.1:8787/health' 2>/dev/null)
  fi

  case "$gw" in active) gw_s="ON";; inactive) gw_s="off";; failed) gw_s="FAIL";; *) gw_s="?";; esac
  case "$rg" in active) rg_s="ON";; inactive) rg_s="off";; failed) rg_s="FAIL";; *) rg_s="?";; esac

  if [ -z "$health" ]; then
    report="${report}**${name}:** GW:${gw_s} RG:${rg_s} -- OFFLINE"$'\n'
    continue
  fi

  parsed=$(echo "$health" | python3 "$PARSER" 2>/dev/null)
  report="${report}**${name}:** GW:${gw_s} RG:${rg_s}"$'\n'"\`\`\`"$'\n'"${parsed}"$'\n'"\`\`\`"$'\n'
done

msg="**Fleet Status** ${timestamp}"$'\n'"${report}"

if [ -n "$DISCORD_BOT_TOKEN" ]; then
  json_msg=$(echo "$msg" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")
  curl -s -X POST "https://discord.com/api/v10/channels/${JARVIS_CHANNEL}/messages" \
    -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"content\": ${json_msg}}" > /dev/null 2>&1
fi

echo "$(date -Iseconds) fleet status sent" >> "$LOG"
