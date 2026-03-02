name: haplo-create-pr
description: "Create branch, commit changes, push, and open a pull request"
args:
  repo_path:
    description: "Local path to repository on disk"
    type: string
  branch:
    description: "New branch name"
    type: string
  title:
    description: "PR title and commit message"
    type: string
  body:
    description: "PR body (markdown)"
    type: string
    default: ""
  base:
    description: "Base branch to merge into"
    type: string
    default: "main"
steps:
  - id: create_branch
    description: "Create and switch to new branch"
    command: |
      set -e
      cd "${repo_path}"
      git checkout -b "${branch}" 2>&1
      echo "Branch ${branch} created"
    timeoutMs: 15000

  - id: stage_changes
    description: "Stage all changes"
    command: |
      set -e
      cd "${repo_path}"
      git add -A 2>&1
      changed=$(git diff --cached --stat | tail -1)
      echo "Staged: $changed"
    timeoutMs: 15000

  - id: commit
    description: "Commit staged changes"
    command: |
      set -e
      cd "${repo_path}"
      git commit -m "${title}" 2>&1
    timeoutMs: 15000

  - id: push
    description: "Push branch to origin"
    command: |
      set -e
      cd "${repo_path}"
      git push -u origin "${branch}" 2>&1
    timeoutMs: 30000

  - id: create_pr
    description: "Create the pull request"
    command: |
      set -e
      cd "${repo_path}"
      repo_name=$(gh repo view --json nameWithOwner -q .nameWithOwner)
      gh pr create --repo "${repo_name}" --base "${base}" --head "${branch}" --title "${title}" --body "${body}" 2>&1
      echo ""
      echo "=== HAPLO CREATE-PR COMPLETE ==="
    timeoutMs: 30000