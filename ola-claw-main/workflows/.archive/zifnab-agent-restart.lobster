name: zifnab-agent-restart
description: "Securely restart an OpenClaw agent's gateway on a target server"
args:
  target_host:
    description: "Tailscale IP of the target server (e.g., [REDACTED_TS_IP] for Haplo)"
    type: string
  agent_name:
    description: "Name of the agent to restart (e.g., Haplo, Hugh)"
    type: string
steps:
  - id: restart_gateway
    description: "Restarting OpenClaw gateway for target agent"
    command: ssh openclaw@${target_host} "systemctl --user restart openclaw-gateway"
    timeoutMs: 30000
