
name: haplo-deploy-service
description: Restarts a systemd service on a target server via SSH.
parameters:
  target_host:
    type: string
    description: Tailscale IP or hostname of the target server (e.g., [REDACTED_TS_IP] for ola-claw-trade).
  service_name:
    type: string
    description: Name of the systemd service to restart (e.g., patryn-trader).
steps:
  - name: Restart service on target host
    exec:
      command: ssh openclaw@"${{ parameters.target_host }}" "sudo systemctl restart ${{ parameters.service_name }}"
      description: SSH into the target host and restart the specified systemd service.
