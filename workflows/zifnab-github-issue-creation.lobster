name: zifnab-github-issue-creation
description: "Standardized creation of GitHub issues with labels and assignees"
args:
  repo:
    description: "Repository name (e.g. Pryan-Fire)"
    type: string
  title:
    description: "Issue title"
    type: string
  body:
    description: "Issue body (markdown)"
    type: string
    default: ""
  labels:
    description: "Comma-separated label names"
    type: string
    default: ""
  assignees:
    description: "Comma-separated GitHub usernames to assign"
    type: string
    default: ""
steps:
  - id: create_issue
    description: "Create the GitHub issue"
    command: |
      set -e
      cmd="gh issue create --repo The-Nexus-Decoded/${repo} --title \"${title}\" --body \"${body}\""
      if [ -n "${labels}" ]; then
        cmd="$cmd --label ${labels}"
      fi
      if [ -n "${assignees}" ]; then
        cmd="$cmd --assignee ${assignees}"
      fi
      eval $cmd 2>&1
      echo ""
      echo "=== ZIFNAB ISSUE CREATED ==="
    timeoutMs: 30000