#!/bin/bash
# Rebuild your dashboard from your weekN/ work. Never opens a tab —
# refresh your dashboard tab to see the result (or open one with
# ./start_dashboard.sh).
#     ./rebuild_dashboard.sh

LOG=/tmp/dashboard-server.log
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$WORKSPACE_DIR/make_manifest.py" --build || exit 1

# Silently make sure the preview server is up so "refresh" always works.
if ! curl -fs -o /dev/null "http://localhost:8000/"; then
    nohup python3 "$WORKSPACE_DIR/make_manifest.py" --serve >> "$LOG" 2>&1 &
fi

echo
echo "Dashboard rebuilt — refresh your dashboard tab (or run ./start_dashboard.sh to open one)."
