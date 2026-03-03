
name: haplo-create-pr
description: Creates a new branch, commits changes, pushes to remote, and opens a pull request.
parameters:
  repo_path:
    type: string
    description: Absolute path to the repository.
  branch_name:
    type: string
    description: Name of the new branch to create.
  commit_message:
    type: string
    description: Commit message for the changes.
  pr_title:
    type: string
    description: Title for the pull request.
  pr_body:
    type: string
    description: Body/description for the pull request.
steps:
  - name: Create new branch
    exec:
      command: git -C "${{ parameters.repo_path }}" checkout -b "${{ parameters.branch_name }}"
      description: Create and switch to a new branch.
  - name: Add all changes
    exec:
      command: git -C "${{ parameters.repo_path }}" add .
      description: Stage all changes in the repository.
  - name: Commit changes
    exec:
      command: git -C "${{ parameters.repo_path }}" commit -m "${{ parameters.commit_message }}"
      description: Commit the staged changes.
  - name: Push to remote
    exec:
      command: git -C "${{ parameters.repo_path }}" push -u origin "${{ parameters.branch_name }}"
      description: Push the new branch and its commits to the remote repository.
  - name: Open Pull Request
    exec:
      command: gh pr create --repo The-Nexus-Decoded/Pryan-Fire --base main --head "${{ parameters.branch_name }}" --title "${{ parameters.pr_title }}" --body "${{ parameters.pr_body }}"
      description: Open a new pull request on GitHub.
