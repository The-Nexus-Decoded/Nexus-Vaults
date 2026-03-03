name: haplo-deploy-service
description: "Deploy a service by restarting its systemd unit on a target server"
args:
  service_name:
    description: "Systemd service name (e.g., openclaw-gateway)"
    type: string
  target_host:
    description: "Tailscale IP of target server"
    type: string
steps:
  - id: restart_service
    description: "Restarting service on target"
    command: ssh openclaw@${target_host} "systemctl --user restart ${service_name}"
    timeoutMs: 30000
