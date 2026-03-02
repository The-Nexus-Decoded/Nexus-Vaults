name: zifnab-memory-maintenance
description: "Gather recent daily memory files for review and distillation"
args:
  days:
    description: "Number of recent days to gather (including today)"
    type: integer
    default: 7
  workspace:
    description: "Workspace path containing memory directory"
    type: string
    default: "/data/openclaw/workspace"
steps:
  - id: list_files
    description: "List available memory files"
    command: |
      set -e
      MEMDIR="${workspace}/memory"
      echo "Memory directory: ${MEMDIR}"
      ls -1tr "${MEMDIR}"/*.md 2>/dev/null | tail -${days} || echo "No memory files found"
    timeoutMs: 10000

  - id: gather
    description: "Concatenate recent memory files"
    command: |
      set -e
      MEMDIR="${workspace}/memory"
      if [ ! -d "${MEMDIR}" ]; then
        echo "ERROR: Memory directory not found: ${MEMDIR}"
        exit 1
      fi
      FILES=$(ls -1tr "${MEMDIR}"/*.md 2>/dev/null | tail -${days})
      if [ -z "${FILES}" ]; then
        echo "No memory files to gather"
        exit 0
      fi
      echo "=== GATHERING MEMORY FILES ==="
      for f in ${FILES}; do
        echo "--- $(basename "$f") ---"
        cat "$f"
        echo ""
      done
      echo "=== MEMORY GATHER COMPLETE ==="
    timeoutMs: 10000

  - id: summary
    description: "Show file count and total size"
    command: |
      set -e
      MEMDIR="${workspace}/memory"
      if [ -d "${MEMDIR}" ]; then
        echo "Memory files (last ${days} days):"
        ls -lh "${MEMDIR}"/*.md 2>/dev/null | tail -${days} | awk '{print $5, $9}'
        total=$(ls -1 "${MEMDIR}"/*.md 2>/dev/null | wc -l)
        echo "Total memory files: ${total}"
      fi
    timeoutMs: 5000