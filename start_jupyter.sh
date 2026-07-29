#!/bin/bash
# Open the classic Jupyter Notebook server in a browser tab, starting the
# server first if it isn't running. The Codespace starts the server on
# launch (on_start.sh runs this with --no-open), so the usual run just
# opens the tab:
#     ./start_jupyter.sh
# Safe to run any time.

LOG=/tmp/jupyter-server.log

# Workspace root = this script's directory; the CSP-free files handler
# lives in .devcontainer/.
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVCONTAINER_DIR="$WORKSPACE_DIR/.devcontainer"

server_up() {
    curl -fs -o /dev/null "http://localhost:8888/tree"
}

if ! server_up; then
    echo "=== start_jupyter.sh $(date) ===" >> "$LOG"
    # --allow-origin='*' : allow the Codespace forwarded URL to load
    #   /files/*.html plot previews (else 403 cross-origin / unknown-origin).
    #   --root_dir : serve the course tree, not $HOME.
    # files_handler_class + PYTHONPATH: serve /files/ without the CSP sandbox
    #   so MP4 preview links play behind the private forwarded port (see
    #   .devcontainer/course_files_handler.py for the full story).
    PYTHONPATH="$DEVCONTAINER_DIR${PYTHONPATH:+:$PYTHONPATH}" \
    nohup jupyter nbclassic \
        --allow-root \
        --ip=0.0.0.0 \
        --port=8888 \
        --no-browser \
        --IdentityProvider.token='' \
        --ServerApp.password='' \
        --ServerApp.allow_origin='*' \
        --ServerApp.root_dir="$WORKSPACE_DIR" \
        --ContentsManager.files_handler_class=course_files_handler.NoSandboxFilesHandler \
        >> "$LOG" 2>&1 &
    echo "Starting Jupyter server on port 8888..."
    STARTED=0
    for _ in $(seq 1 30); do
        if server_up; then
            STARTED=1
            break
        fi
        sleep 1
    done
    if [ "$STARTED" -ne 1 ]; then
        echo "Jupyter server FAILED to start — last log lines:" >&2
        tail -20 "$LOG" >&2
        exit 1
    fi
fi

if [ "$1" = "--no-open" ]; then
    # Codespace-launch mode: just make sure the server is up.
    echo "Jupyter server running on port 8888"
    exit 0
fi

if [ -n "$CODESPACE_NAME" ] && [ -n "$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN" ]; then
    URL="https://${CODESPACE_NAME}-8888.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/"
else
    URL="http://localhost:8888/"
fi
echo "Jupyter is running at $URL"
if [ -n "$BROWSER" ]; then
    "$BROWSER" "$URL"
fi
echo 'If no tab appears: run ./start_jupyter.sh again, or click the world icon on the "Jupyter" port in the Ports tab.'
