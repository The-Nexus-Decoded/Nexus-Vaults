
name: zifnab-agent-restart
description: Securely restarts an OpenClaw gateway using the seventh-gate workflow.
parameters:
  target_agent_id:
    type: string
    description: The ID of the agent whose gateway needs to be restarted.
steps:
  - name: Run seventh-gate for secure restart
    lobster:
      action: run
      pipeline: /data/openclaw/workspace/workflows/seventh-gate.lobster
      argsJson: "{\"target_agent_id\": \"${{ parameters.target_agent_id }}\"}"
      description: Initiates the secure gateway restart process.
