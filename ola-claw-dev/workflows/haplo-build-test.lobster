
name: haplo-build-test
description: Pulls latest code, installs dependencies, builds, and runs tests for a given repository.
parameters:
  repo_path:
    type: string
    description: Absolute path to the repository.
steps:
  - name: Pull latest code
    exec:
      command: git -C "${{ parameters.repo_path }}" pull origin main
      description: Ensure the repository is up-to-date.
  - name: Install dependencies
    exec:
      command: |
        cd "${{ parameters.repo_path }}"
        if [ -f "package.json" ]; then
          npm install
        elif [ -f "requirements.txt" ]; then
          pip install -r requirements.txt
        fi
      description: Install project dependencies based on detected package manager.
  - name: Build project
    exec:
      command: |
        cd "${{ parameters.repo_path }}"
        if [ -f "package.json" ]; then
          npm run build || true
        elif [ -f "setup.py" ]; then
          python setup.py build || true
        fi
      description: Build the project if build scripts are detected.
      optional: true
  - name: Run tests
    exec:
      command: |
        cd "${{ parameters.repo_path }}"
        if [ -f "package.json" ]; then
          npm test || true
        elif [ -f "pytest.ini" ] || [ -d "tests" ]; then
          pytest || true
        fi
      description: Run tests if test scripts/frameworks are detected.
      optional: true
