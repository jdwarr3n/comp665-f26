"""Files handler without the CSP sandbox directive.

Jupyter Server's FilesHandler appends "; sandbox allow-scripts" to the
Content-Security-Policy of everything served under /files/. The sandbox
puts a browser's internal video-player page in an opaque origin, so its
media re-fetch is sent without cookies — and behind a private Codespace
forwarded port (which authenticates every request with a GitHub cookie)
that request is rejected: MP4 preview links show a dead black player.

Dropping the sandbox keeps /files/ same-origin, so the proxy cookie
flows and the course preview links (week 4 MP4s, weeks 12-14 plotly
HTML) work. Security trade-off, accepted for this course: served
content is the student's own repo in their own single-user server, so
un-sandboxed scripts are self-inflicted only.

Wired up in start_jupyter.sh (repo root) via
  --ContentsManager.files_handler_class=course_files_handler.NoSandboxFilesHandler
"""

from jupyter_server.files.handlers import FilesHandler


class NoSandboxFilesHandler(FilesHandler):
    @property
    def content_security_policy(self):
        # The default from the base JupyterHandler (frame-ancestors +
        # report-uri), minus FilesHandler's "; sandbox allow-scripts".
        csp = super().content_security_policy
        return "; ".join(
            part for part in csp.split("; ") if not part.startswith("sandbox")
        )
