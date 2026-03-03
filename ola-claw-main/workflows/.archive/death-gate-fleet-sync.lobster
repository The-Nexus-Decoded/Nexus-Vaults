name: death-gate-fleet-sync
description: "Fleet-wide repository synchronization using fleet workspace-sync"
args:
  files:
    description: "Comma-separated files to sync (default: TOOLS.md,MEMORY.md)"
    type: string
    default: "TOOLS.md,MEMORY.md"
steps:
  - id: sync
    description: "Sync workspace files across fleet"
    command: fleet workspace-sync --json --from zifnab --to haplo,hugh --files ${files}
    timeoutMs: 60000

  - id: report
    description: "Show sync results"
    command: fleet format
    stdin: $sync.stdout
    timeoutMs: 10000
