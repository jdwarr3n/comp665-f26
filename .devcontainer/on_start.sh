#!/bin/bash
# Codespace launch (postStartCommand): bring up the course servers silently.
# No browser tabs are opened here — the popup would be blocked anyway
# (browsers only open tabs right after a keypress); students open the tabs
# with ./start_jupyter.sh and ./start_dashboard.sh.

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

bash "$WORKSPACE_DIR/start_jupyter.sh" --no-open

if ! curl -fs -o /dev/null "http://localhost:8000/"; then
    nohup python3 "$WORKSPACE_DIR/make_manifest.py" --serve \
        >> /tmp/dashboard-server.log 2>&1 &
    echo "Dashboard preview server starting on port 8000"
    # Wait until it answers before exiting — a background child still
    # starting when this script returns gets killed with the postStart
    # process cleanup (observed 2026-07-19: empty log, no process).
    for _ in $(seq 1 15); do
        if curl -fs -o /dev/null "http://localhost:8000/"; then
            echo "Dashboard preview server running on port 8000"
            exit 0
        fi
        sleep 1
    done
    echo "Dashboard preview server FAILED to start — last log lines:" >&2
    tail -20 /tmp/dashboard-server.log >&2
    exit 1
fi
