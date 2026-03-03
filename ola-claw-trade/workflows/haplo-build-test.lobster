name: haplo-build-test
description: "Run tests and linting on a project using fleet gauntlet"
args:
  repo_path:
    description: "Path to the repository directory (e.g., /data/repos/Pryan-Fire)"
    type: string
steps:
  - id: test
    description: "Run gauntlet (auto-detects project type, runs tests + lint)"
    command: fleet gauntlet --json --target ${repo_path}
    timeoutMs: 300000

  - id: report
    description: "Format test results"
    command: fleet format gauntlet-report
    stdin: $test.stdout
    timeoutMs: 10000
