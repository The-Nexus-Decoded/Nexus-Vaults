name: zifnab-agent-restart
description: "Safely restart an OpenClaw agent gateway with pre-flight and verification"
args:
  host:
    description: "Target host (Tailscale IP or hostname)"
    type: string
  user:
    description: "SSH user on target host"
    type: string
    default: "openclaw"
  agent_label:
    description: "Agent label (for logging purposes)"
    type: string
    default: "agent"
steps:
  - id: preflight
    description: "Check gateway status before restart"
    command: |
      set -e
      echo "Target: ${user}@${host} (${agent_label})"
      ssh ${user}@${host} "systemctl --user status openclaw-gateway --no-pager -n 5" 2>&1
    timeoutMs: 15000

  - id: restart
    description: "Restart the gateway service"
    command: |
      set -e
      ssh ${user}@${host} "systemctl --user restart openclaw-gateway" 2>&1
      echo "Restart command sent"
    timeoutMs: 15000

  - id: wait
    description: "Wait for startup"
    command: |
      set -e
      echo "Waiting 10 seconds for startup..."
      sleep 10
    timeoutMs: 15000

  - id: verify
    description: "Check health endpoint"
    command: |
      set -e
      if ssh ${user}@${host} "curl -s http://127.0.0.1:18789/health" 2>&1 | grep -q '"healthy":true'; then
        echo "Gateway is healthy"
      else
        echo "WARNING: Health check did not return healthy status"
      fi
      ssh ${user}@${host} "systemctl --user status openclaw-gateway --no-pager -n 10" 2>&1
      echo ""
      echo "=== ZIFNAB AGENT RESTART COMPLETE ==="
    timeoutMs: 20000