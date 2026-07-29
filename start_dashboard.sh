#!/bin/bash
# Open your dashboard in a browser tab, starting the preview server first
# if it isn't running. The Codespace starts the server on launch, so the
# usual run just opens the tab:
#     ./start_dashboard.sh
# Safe to run any time. The tab shows the dashboard as of the last build —
# run ./rebuild_dashboard.sh (then refresh) to see new work.

LOG=/tmp/dashboard-server.log
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

server_up() {
    curl -fs -o /dev/null "http://localhost:8000/"
}

if ! server_up; then
    nohup python3 "$WORKSPACE_DIR/make_manifest.py" --serve >> "$LOG" 2>&1 &
    echo "Starting the dashboard preview server on port 8000..."
    STARTED=0
    for _ in $(seq 1 15); do
        if server_up; then
            STARTED=1
            break
        fi
        sleep 1
    done
    if [ "$STARTED" -ne 1 ]; then
        echo "Dashboard preview server FAILED to start — last log lines:" >&2
        tail -20 "$LOG" >&2
        exit 1
    fi
fi

if [ -n "$CODESPACE_NAME" ] && [ -n "$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN" ]; then
    URL="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/"
else
    URL="http://localhost:8000/"
fi
echo "Dashboard is served at $URL"
if [ -n "$BROWSER" ]; then
    "$BROWSER" "$URL"
fi
echo 'If no tab appears: run ./start_dashboard.sh again, or click the world icon on the "Dashboard preview" port in the Ports tab.'
