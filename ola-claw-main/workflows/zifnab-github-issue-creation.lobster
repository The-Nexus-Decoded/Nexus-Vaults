
name: zifnab-github-issue-creation
description: Standardizes GitHub issue creation for a specified repository.
parameters:
  repo_name:
    type: string
    description: Name of the GitHub repository (e.g., The-Nexus-Decoded/Pryan-Fire).
  issue_title:
    type: string
    description: Title of the new GitHub issue.
  issue_body:
    type: string
    description: Body/description of the new GitHub issue.
  issue_labels:
    type: string
    description: Comma-separated list of labels for the issue (optional).
    optional: true
steps:
  - name: Create GitHub Issue
    exec:
      command: |
        if [ -n "${{ parameters.issue_labels }}" ]; then
          gh issue create --repo ${{ parameters.repo_name }} --title "${{ parameters.issue_title }}" --body "${{ parameters.issue_body }}" --label "${{ parameters.issue_labels }}"
        else
          gh issue create --repo ${{ parameters.repo_name }} --title "${{ parameters.issue_title }}" --body "${{ parameters.issue_body }}"
        fi
      description: Create a new issue in the specified GitHub repository.
