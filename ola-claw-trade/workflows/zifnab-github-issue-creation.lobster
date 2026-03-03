name: zifnab-github-issue-creation
description: "Create a new GitHub issue in a specified repository"
args:
  repo_name:
    description: "Repository name (e.g., Pryan-Fire, Chelestra-Sea)"
    type: string
  title:
    description: "Issue title"
    type: string
  body:
    description: "Issue body (markdown)"
    type: string
    default: ""
  labels:
    description: "Comma-separated labels"
    type: string
    default: "task"
steps:
  - id: create_issue
    description: "Creating the GitHub issue"
    command: gh issue create --repo The-Nexus-Decoded/${repo_name} --title "${title}" --body "${body}" --label "${labels}"
    timeoutMs: 60000
