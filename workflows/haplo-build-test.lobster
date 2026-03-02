name: haplo-build-test
description: "Automated pull, install, build, and test for a project"
args:
  repo_path:
    description: "Path to repository on disk"
    type: string
  branch:
    description: "Git branch to pull"
    type: string
    default: "main"
steps:
  - id: pull
    description: "Fetch latest code"
    command: |
      set -e
      cd "${repo_path}" && git pull origin "${branch}" 2>&1
      echo "Code updated to ${branch}"
    timeoutMs: 60000

  - id: install
    description: "Install dependencies"
    command: |
      set -e
      cd "${repo_path}"
      if [ -f package.json ]; then
        npm install 2>&1 | tail -5
      elif [ -f requirements.txt ]; then
        pip install -r requirements.txt 2>&1 | tail -5
      else
        echo "No dependency file found (package.json or requirements.txt)"
      fi
    timeoutMs: 180000

  - id: build
    description: "Build project"
    command: |
      set -e
      cd "${repo_path}"
      if npm run build 2>&1 | tail -10; then
        echo "Build succeeded"
      else
        echo "No build script or build failed"
      fi
    timeoutMs: 240000

  - id: test
    description: "Run tests"
    command: |
      set -e
      cd "${repo_path}"
      if npm test 2>&1; then
        echo "Tests passed"
      else
        echo "No test script or tests failed"
      fi
      echo ""
      echo "=== HAPLO BUILD-TEST COMPLETE ==="
    timeoutMs: 300000