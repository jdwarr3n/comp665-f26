# COMP 665 frozen course environment — Python 3.10, package set from the
# desktop freeze (.devcontainer/lockfile-freeze-py310.txt). See
# comp665-private/docs/planning/comp665-codespace.md.
FROM python:3.10-bookworm

# ffmpeg: matplotlib animation writer for the week 4 MP4s (desktop had a
# separate ffmpeg install; pip packages don't provide the binary).
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# The lockfile is a Windows `pip freeze`; pywin32 and pywinpty have no Linux
# packages and are Windows-only Jupyter deps (Linux uses ptyprocess, already
# in the set). Filter at build time so the lockfile stays the single record.
COPY .devcontainer/lockfile-freeze-py310.txt /tmp/lockfile-win.txt
RUN grep -vE '^(pywin32|pywinpty)==' /tmp/lockfile-win.txt > /tmp/lockfile-linux.txt \
    && pip install --no-cache-dir -r /tmp/lockfile-linux.txt \
    && rm /tmp/lockfile-win.txt /tmp/lockfile-linux.txt

# JupyterLab is NOT in the desktop freeze (desktop ran classic notebook 6 via
# Thonny). 3.6.8 is the last 3.x release; compatible with this jupyter stack.
RUN pip install --no-cache-dir jupyterlab==3.6.8

EXPOSE 8888
