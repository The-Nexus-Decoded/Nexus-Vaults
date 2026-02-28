# Agent Heartbeat Monitor

This script monitors the health and activity of agent sessions across the fleet. It periodically checks the status of active sessions and logs warnings for any that have been inactive for longer than a specified threshold.

## Features

-   Periodically lists active agent sessions.
-   Calculates the inactivity duration for each session.
-   Logs warnings for sessions inactive for more than 60 minutes.
-   (Future enhancement) Notifies the `#jarvis` channel about inactive sessions.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd agent-heartbeat-monitor
    ```

2.  **Install Dependencies:**
    This script is written in Python and does not have external dependencies beyond what's available in the OpenClaw environment (specifically the `default_api` for `sessions_list`). Ensure your environment has Python 3.x.

3.  **Configure:**
    -   `INACTIVITY_THRESHOLD_MINUTES`: Set the inactivity threshold in minutes (default is 60).
    -   `JARVIS_CHANNEL_ID`: If you intend to integrate with a notification system for `#jarvis`, update this variable.

## Usage

To run the script manually:

```bash
python monitor.py
```

The script will output its findings to the console, including information about active sessions and warnings for inactive ones.

## Logging

The script uses Python's built-in `logging` module. Logs are output to the console by default.

## Notifications

Currently, inactive sessions are logged as warnings. To enable notifications to the `#jarvis` channel, you would need to integrate with the `message` tool or a similar notification service. The placeholder `log_notification_for_jarvis` function in `monitor.py` shows where this integration would occur.

## Contributing

Contributions are welcome! Please follow the established contribution guidelines and development workflow for The-Nexus-Decoded projects.
