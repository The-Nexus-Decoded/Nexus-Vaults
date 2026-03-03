name: hughs-forge-deploy
description: "Deploy hughs-forge to ola-claw-trade: test, deliver, restart"
args:
  repo:
    description: "Repository name (e.g., Pryan-Fire)"
    type: string
    default: "Pryan-Fire"
  branch:
    description: "Branch to deliver"
    type: string
    default: "main"
  target_path:
    description: "Path to repo on target server"
    type: string
    default: "/data/repos/Pryan-Fire"
steps:
  - id: test
    description: "Run gauntlet on the repo"
    command: fleet gauntlet --json --target ${target_path}
    timeoutMs: 300000

  - id: review
    description: "Review test results before deploy"
    command: |
      echo "========================================="
      echo "  HUGHS FORGE DEPLOY"
      echo "========================================="
      echo ""
      fleet format gauntlet-report
      echo ""
      echo "Approve to deliver and restart on Hugh."
    stdin: $test.stdout
    approval: required
    timeoutMs: 10000

  - id: deliver
    description: "Git deliver to Hugh"
    command: fleet deliver --json --repo ${repo} --branch ${branch} --message "Deploy hughs-forge via workflow"
    timeoutMs: 60000

  - id: verify
    description: "Verify health after deploy"
    command: fleet health --json | fleet format
    timeoutMs: 15000
