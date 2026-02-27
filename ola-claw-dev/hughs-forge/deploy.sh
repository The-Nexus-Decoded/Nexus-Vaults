#!/bin/bash
set -e

# Deployment Script for Hugh's Trading Pipeline
# Target: ola-claw-trade

# --- Configuration ---
REPO_URL="https://github.com/The-Nexus-Decoded/Pryan-Fire.git"
DEPLOY_DIR="/data/openclaw/services/hughs-trading-pipeline"
REPO_DIR="$DEPLOY_DIR/Pryan-Fire"
SERVICE_DIR="$REPO_DIR/hughs-forge"
PYTHON_VENV="$DEPLOY_DIR/venv"

# --- Main ---
echo "--- Starting deployment to $DEPLOY_DIR ---"

# 1. Create deployment directory
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# 2. Clone or update repository
if [ -d "$REPO_DIR" ]; then
    echo "--- Repository exists, pulling latest changes ---"
    cd $REPO_DIR
    git pull
else
    echo "--- Cloning repository ---"
    git clone $REPO_URL
fi

# 3. Set up Python environment
echo "--- Setting up Python virtual environment ---"
if [ -d "$PYTHON_VENV" ]; then
    echo "Virtual environment exists."
else
    python3 -m venv $PYTHON_VENV
fi
source $PYTHON_VENV/bin/activate

echo "--- Installing Python dependencies ---"
pip install -r $SERVICE_DIR/requirements.txt # Assuming a requirements.txt will be created

# 4. Set up TypeScript environment (assuming TS files are in services/)
echo "--- Setting up TypeScript environment ---"
TS_SERVICE_PATH="$SERVICE_DIR/services/trade-executor" # This path needs verification
cd $TS_SERVICE_PATH

if [ -f "package.json" ]; then
    echo "--- Installing Node.js dependencies ---"
    npm install
else
    echo "--- WARNING: package.json not found in $TS_SERVICE_PATH. Skipping npm install. ---"
fi

# 5. Finalize
echo "--- Deployment complete ---"
echo "To run the service:"
echo "1. SSH to ola-claw-trade"
echo "2. Populate the .env file at $SERVICE_DIR/.env with the devnet wallet key"
echo "3. Activate the environment: source $PYTHON_VENV/bin/activate"
echo "4. Run the master script: python $SERVICE_DIR/main.py"

exit 0
