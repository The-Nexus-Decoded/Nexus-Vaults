name: fleet-status
description: "Aggregate health status from all 3 fleet servers using fleet CLI"
steps:
  - id: health
    description: "Get fleet health from rate guard"
    command: fleet health --json
    timeoutMs: 15000

  - id: report
    description: "Format health report"
    command: fleet format health-report
    stdin: $health.stdout
    timeoutMs: 10000
