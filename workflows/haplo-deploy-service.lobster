name: haplo-deploy-service
description: "Deploy a service by restarting its systemd unit on a target server"
args:
  service:
    description: "Systemd service name to restart"
    type: string
  host:
    description: "Target host (Tailscale IP or hostname)"
    type: string
  user:
    description: "SSH user on target host"
    type: string
    default: "openclaw"
  use_sudo:
    description: "Use sudo for systemctl commands"
    type: boolean
    default: true
steps:
  - id: preflight
    description: "Check service status before restart"
    command: |
      set -e
      echo "Target: ${user}@${host}"
      echo "Service: ${service}"
      ssh ${user}@${host} "systemctl status '${service}' --no-pager -n 5" 2>&1 || echo "Service may not exist or is not active"
    timeoutMs: 15000

  - id: restart
    description: "Restart the service"
    command: |
      set -e
      if [ "${use_sudo}" = "true" ]; then
        ssh ${user}@${host} "sudo systemctl restart '${service}'" 2>&1
      else
        ssh ${user}@${host} "systemctl restart '${service}'" 2>&1
      fi
      echo "Service restart initiated"
    timeoutMs: 15000

  - id: verify
    description: "Check service status after restart"
    command: |
      set -e
      sleep 3
      ssh ${user}@${host} "systemctl status '${service}' --no-pager -n 10" 2>&1
      echo ""
      echo "=== HAPLO DEPLOY-SERVICE COMPLETE ==="
    timeoutMs: 15000