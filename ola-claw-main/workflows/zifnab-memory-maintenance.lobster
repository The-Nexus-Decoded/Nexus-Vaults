
name: zifnab-memory-maintenance
description: Gathers recent memory files for review and provides their content.
steps:
  - name: List recent memory files
    exec:
      command: find /data/openclaw/workspace/memory -maxdepth 1 -type f -name '2026-03*.md' -o -name '2026-02*.md' | sort -r
      description: List memory files from current and previous month.
    output_to_param: recent_memory_files
  - name: Read and concatenate memory files
    exec:
      command: |
        if [ -n "${{ outputs.recent_memory_files }}" ]; then
          for file in ${{ outputs.recent_memory_files }}; do
            echo "--- $file ---"
            cat "$file"
            echo "\n"
          done
        else
          echo "No recent memory files found."
        fi
      description: Read the content of the identified memory files.
