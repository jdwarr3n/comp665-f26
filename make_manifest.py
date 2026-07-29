#!/usr/bin/env python3
"""COMP 665 course tool: build the dashboard and generate the Canvas submission manifest.

Telemetry is stubbed (not built yet). A submission run commits your work
and then pushes it to GitHub: the push is what publishes your dashboard
(GitHub Pages) and makes the pinned version fetchable by the grader. If
the push fails, the manifest is still valid — the version is fixed at
commit — but stays unpublished until you run `git push` yourself.
Design record: comp665-private docs/dashboard-notes.md.

Usage:
  python3 make_manifest.py N                  submission run for week N:
                                              extract, rebuild, commit, and
                                              write/print the manifest
  python3 make_manifest.py --extract [N]      extract steps only
  python3 make_manifest.py --build            extract all weeks + rebuild pages
  python3 make_manifest.py --serve            persistent preview server (no build)
  --force                                     ignore freshness dates (repair)
  --port P                                    preview port (default 8000)

Running this script does not submit anything: pasting the manifest into
the Canvas text-entry box is the submission. Open weekN/projectN_manifest.md
in a markdown preview and copy the rendered manifest (the dashboard link
must be clickable for your peer reviewers).

The dashboard tree under docs/ is machine-written: students author their
work in weekN/ (notebook, projectN_development.md) and never edit docs/
by hand.
"""

import argparse
import base64
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# The manifest and progress output use ✓ etc.; keep working on consoles
# with legacy encodings (Windows cp1252) instead of crashing.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

FIRST_WEEK, LAST_WEEK = 2, 14
REPO_ROOT = Path(__file__).resolve().parent
DOCS = REPO_ROOT / "docs"
PLOT_NAME_PREFIXES = ("test_plot_", "plot_", "test_")


def write_if_changed(path, data):
    """Write bytes only when the content differs (keeps rebuilds churn-free)."""
    if path.exists() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True


# --------------------------------------------------------------------------
# step 1 — extract_plots: embedded PNGs from the solution notebook
# --------------------------------------------------------------------------

def extract_plots(week, force=False):
    """Extract embedded PNGs from weekN/projectN_solution.ipynb into
    docs/weekN/plots/.

    Naming rule: each image cell's first `def` (trimmed of the
    test_plot_/plot_/test_ prefix) names its files, with a _1.._n suffix in
    output order. HTML/MP4 artifacts are not extracted — the notebooks save
    those directly into docs/weekN/plots/.

    Freshness: extracted PNGs are stamped with the notebook's mtime; the
    week is skipped when the newest PNG is at least as new as the notebook.

    Returns: None if the notebook is missing, the string "up-to-date" if
    skipped, else the number of extracted images.
    """
    nb_path = REPO_ROOT / f"week{week}" / f"project{week}_solution.ipynb"
    if not nb_path.exists():
        return None
    plots_dir = DOCS / f"week{week}" / "plots"
    nb_mtime = nb_path.stat().st_mtime

    if not force and plots_dir.exists():
        pngs = list(plots_dir.glob("*.png"))
        if pngs and max(p.stat().st_mtime for p in pngs) >= nb_mtime:
            return "up-to-date"

    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    written = set()
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        images = [
            o["data"]["image/png"]
            for o in cell.get("outputs", [])
            if "image/png" in o.get("data", {})
        ]
        if not images:
            continue
        defs = re.findall(r"^def (\w+)", "".join(cell["source"]), re.M)
        if not defs:
            print(f"week{week}: WARNING image cell with no def — skipped")
            continue
        name = defs[0]
        for prefix in PLOT_NAME_PREFIXES:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        for n, img in enumerate(images, 1):
            filename = f"{name}_{n}.png"
            if filename in written:
                print(f"week{week}: WARNING duplicate plot name {filename} — overwritten")
            written.add(filename)
            target = plots_dir / filename
            write_if_changed(target, base64.b64decode(img))
            os.utime(target, (nb_mtime, nb_mtime))
    return len(written)


# --------------------------------------------------------------------------
# step 2 — extract_report: render the development report into docs/
# --------------------------------------------------------------------------

def render_markdown(text):
    """Markdown → HTML; degrade to preformatted text without the markdown
    package (the course image ships it)."""
    try:
        import markdown
        return markdown.markdown(text, extensions=["tables", "fenced_code"])
    except ImportError:
        return f"<pre>{html.escape(text)}</pre>"


def extract_report(week, force=False):
    """Render weekN/projectN_development.md into
    docs/weekN/projectN_development.html — a body fragment (the week page
    supplies the surrounding document and styling).

    Freshness: the fragment is stamped with the source's mtime; skipped
    when it is at least as new as the source.

    Returns: None if the source report is missing, the string "up-to-date"
    if skipped, else "rendered".
    """
    src = REPO_ROOT / f"week{week}" / f"project{week}_development.md"
    dst = DOCS / f"week{week}" / f"project{week}_development.html"
    if not src.exists():
        return None
    src_mtime = src.stat().st_mtime
    if not force and dst.exists() and dst.stat().st_mtime >= src_mtime:
        return "up-to-date"
    fragment = render_markdown(src.read_text(encoding="utf-8")) + "\n"
    write_if_changed(dst, fragment.encode("utf-8"))
    os.utime(dst, (src_mtime, src_mtime))
    return "rendered"


# --------------------------------------------------------------------------
# step 3 — build_dashboard: assemble docs/ into week pages + index
# --------------------------------------------------------------------------

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
VIDEO_EXTS = {".mp4", ".webm", ".ogv"}
INTERACTIVE_EXTS = {".html", ".htm"}
DASHBOARD_TITLE = "COMP 665"
DASHBOARD_SUBTITLE = "Data Visualization Portfolio"


def load_titles():
    titles_path = DOCS / "assets" / "project_titles.json"
    if titles_path.exists():
        return json.loads(titles_path.read_text(encoding="utf-8"))
    return {}


def scan_week(week):
    """Collect a week's published items from docs/weekN/ (pure assembly —
    the extract steps have already done all transformation)."""
    week_dir = DOCS / f"week{week}"
    plots_dir = week_dir / "plots"
    items = []
    if plots_dir.exists():
        for asset in sorted(plots_dir.iterdir(), key=lambda p: p.name.lower()):
            if not asset.is_file() or asset.name.startswith("."):
                continue
            ext = asset.suffix.lower()
            if ext in IMAGE_EXTS:
                kind = "image"
            elif ext in VIDEO_EXTS:
                kind = "video"
            elif ext in INTERACTIVE_EXTS:
                kind = "interactive"
            else:
                kind = "file"
            title = asset.stem.replace("_", " ").strip()
            items.append({
                "kind": kind,
                "src": f"plots/{asset.name}",
                "label": title[0].upper() + title[1:] if title else asset.name,
            })
    fragment_path = week_dir / f"project{week}_development.html"
    report = fragment_path.read_text(encoding="utf-8") if fragment_path.exists() else None
    return items, report


def sidebar_html(weeks, active, prefix):
    """The week navigation; prefix is '' on the index page, '../' on week pages."""
    entries = [
        f'<a class="menu-item{" active" if active == 0 else ""}" '
        f'href="{prefix if prefix else "./"}">Overview</a>'
    ]
    for week in weeks:
        cls = " active" if active == week else ""
        entries.append(
            f'<a class="menu-item{cls}" href="{prefix}week{week}/">Week {week}</a>'
        )
    menu = "\n        ".join(entries)
    return f"""
    <nav id="sidebar">
      <div class="sidebar-header">
        <h1>{DASHBOARD_TITLE}</h1>
        <p>{DASHBOARD_SUBTITLE}</p>
      </div>
      <div id="menu">
        {menu}
      </div>
    </nav>"""


def page_html(title, sidebar, header_title, header_subtitle, body, prefix,
              scripts=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
  <div id="app">{sidebar}
    <main id="content">
      <header class="content-header">
        <h2>{html.escape(header_title)}</h2>
        <p>{html.escape(header_subtitle)}</p>
      </header>
{body}
    </main>
  </div>{scripts}
</body>
</html>
"""


def render_week_page(week, weeks, items, report, project_title):
    tabs = ['<button class="tab-item" data-kind="report">Development report</button>']
    for item in items:
        tabs.append(
            f'<button class="tab-item" data-kind="{item["kind"]}" '
            f'data-src="{html.escape(item["src"], quote=True)}">'
            f'{html.escape(item["label"])}</button>'
        )
    tab_bar = "\n            ".join(tabs)
    if report is None:
        report = ("<p class=\"report-missing\">No development report yet — "
                  f"write <code>project{week}_development.md</code> in your "
                  f"<code>week{week}/</code> directory and rerun.</p>")
    body = f"""      <div class="gallery-container">
        <div id="gallery">
          <div class="tab-bar">
            {tab_bar}
          </div>
          <div class="plot-viewer">
            <div id="report-panel" class="report-panel">
{report}
            </div>
            <div id="media-panel" class="media-container"></div>
            <div id="viewer-label" class="viewer-label"></div>
          </div>
        </div>
      </div>"""
    return page_html(
        title=f"Week {week} — {DASHBOARD_TITLE} {DASHBOARD_SUBTITLE}",
        sidebar=sidebar_html(weeks, week, "../"),
        header_title=f"Week {week}",
        header_subtitle=project_title,
        body=body,
        prefix="../",
        scripts='\n  <script src="../assets/app.js"></script>',
    )


def render_index_page(weeks, week_data):
    cards = []
    for week in weeks:
        items = week_data[week]["items"]
        counts = f"{len(items)} plot{'s' if len(items) != 1 else ''}"
        if week_data[week]["report"] is not None:
            counts += " · development report"
        cards.append(f"""          <a class="week-card" href="week{week}/">
            <h3>Week {week}</h3>
            <p>{html.escape(week_data[week]["title"])}</p>
            <span class="badge">{counts}</span>
          </a>""")
    grid = "\n".join(cards) if cards else \
        '          <p class="report-missing">No weeks published yet.</p>'
    body = f"""      <div class="gallery-container scrollable">
        <div class="week-grid">
{grid}
        </div>
      </div>"""
    return page_html(
        title=f"{DASHBOARD_TITLE} {DASHBOARD_SUBTITLE}",
        sidebar=sidebar_html(weeks, 0, ""),
        header_title=DASHBOARD_SUBTITLE,
        header_subtitle="Weekly storytelling plots and development reports",
        body=body,
        prefix="",
    )


def build_dashboard():
    """Assemble docs/ into the dashboard: week pages, landing page, and
    dashboard.json. Reads only what is already under docs/."""
    titles = load_titles()
    week_data = {}
    for week in range(FIRST_WEEK, LAST_WEEK + 1):
        items, report = scan_week(week)
        if not items and report is None:
            continue
        week_data[week] = {
            "items": items,
            "report": report,
            "title": titles.get(f"week{week}", f"Week {week}"),
        }
    weeks = sorted(week_data)

    manifest = {
        "title": f"{DASHBOARD_TITLE} {DASHBOARD_SUBTITLE}",
        "weeks": [
            {
                "week": week,
                "page": f"week{week}/",
                "project_title": week_data[week]["title"],
                "development_report": week_data[week]["report"] is not None,
                "plots": [item["src"] for item in week_data[week]["items"]],
            }
            for week in weeks
        ],
    }
    write_if_changed(DOCS / "dashboard.json",
                     (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"))

    for week in weeks:
        page = render_week_page(
            week, weeks, week_data[week]["items"], week_data[week]["report"],
            week_data[week]["title"],
        )
        write_if_changed(DOCS / f"week{week}" / "index.html", page.encode("utf-8"))

    write_if_changed(DOCS / "index.html",
                     render_index_page(weeks, week_data).encode("utf-8"))
    print(f"dashboard: index + {len(weeks)} week page(s) in {DOCS}")


# --------------------------------------------------------------------------
# serve locally (preview only; never part of a submission run)
# --------------------------------------------------------------------------

def server_running(port):
    import urllib.request
    try:
        urllib.request.urlopen(f"http://localhost:{port}/", timeout=1)
        return True
    except OSError:
        return False


def serve(port):
    """The persistent preview server: serve docs/ straight from disk, so
    rebuilds show up on a tab refresh. Never builds, never opens a browser.
    Started detached at Codespace launch (on_start.sh) and by ensure_server()."""
    from functools import partial
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

    handler = partial(SimpleHTTPRequestHandler, directory=str(DOCS))
    server = ThreadingHTTPServer(("", port), handler)
    print(f"Serving {DOCS} on port {port}")
    server.serve_forever()


def ensure_server(port=8000):
    """Silently make sure the preview server is up. Never opens a tab.
    On failure, prints the server log tail to the terminal (students are
    never pointed at a log file). Returns True if the server is serving."""
    import tempfile
    import time
    if server_running(port):
        return True
    log_path = os.path.join(tempfile.gettempdir(), "dashboard-server.log")
    with open(log_path, "ab") as log:
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()),
             "--serve", "--port", str(port)],
            stdout=log, stderr=log, start_new_session=True)
    for _ in range(15):
        if server_running(port):
            return True
        time.sleep(1)
    print("Dashboard preview server FAILED to start — last log lines:",
          file=sys.stderr)
    try:
        lines = Path(log_path).read_text(encoding="utf-8",
                                         errors="replace").splitlines()
        print("\n".join(lines[-20:]), file=sys.stderr)
    except OSError:
        pass
    return False


# --------------------------------------------------------------------------
# submission run — extract, rebuild, commit + push, write/print the manifest
# --------------------------------------------------------------------------

def git(*args):
    """Run git in the repo root; return stdout, or None on nonzero exit."""
    result = subprocess.run(["git", *args], capture_output=True, text=True,
                            encoding="utf-8", cwd=REPO_ROOT)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def dashboard_url(week):
    """The local preview server's URL for the week page (the manifest links
    to the public Pages URL; this one backs the preview hint). In a
    Codespace, derive the forwarded-port URL so the link is clickable from
    the browser; locally, plain localhost."""
    name = os.environ.get("CODESPACE_NAME")
    domain = os.environ.get("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    if name and domain:
        return f"https://{name}-8000.{domain}/week{week}/"
    return f"http://localhost:8000/week{week}/"


def sweep_telemetry(week):
    """Telemetry sweep + seal (telemetry.md). Not built yet."""
    return "skipped (dev build)"


def commit_all(week):
    """Commit the working tree. Returns the short SHA to pin."""
    if git("add", "-A") is None:
        sys.exit("ERROR: git add failed.")
    if git("diff", "--cached", "--quiet") is None:
        # nonzero exit = staged changes exist
        if git("commit", "-m", f"Project {week} submission") is None:
            sys.exit("ERROR: git commit failed.")
        sha = git("rev-parse", "--short", "HEAD")
        print(f'commit: {sha} "Project {week} submission"')
    else:
        sha = git("rev-parse", "--short", "HEAD")
        print(f"commit: nothing new to commit (HEAD stays {sha})")
    return sha or "no-git"


def push_origin():
    """Push HEAD to origin. Returns True on success. A failed push never
    invalidates the manifest — the SHA is fixed at commit; the push only
    publishes it (dashboard + grader fetch)."""
    return git("push", "origin", "HEAD") is not None


def repo_https_url():
    """https://github.com/<owner>/<repo> from the origin fetch URL, or
    None without a usable GitHub remote."""
    url = git("remote", "get-url", "origin")
    if url is None:
        return None
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url[len("git@github.com:"):]
    if url.endswith(".git"):
        url = url[: -len(".git")]
    if not url.startswith("https://github.com/"):
        return None
    return url


def repo_commit_link(sha):
    """Commit page on GitHub. Works for anyone with repo read
    (instructor/staff); peers without access 404 — fine, the SHA text
    still pins the version."""
    url = repo_https_url()
    return f"{url}/commit/{sha}" if url else None


def pages_url(week):
    """The production dashboard URL (GitHub Pages form), used as the
    manifest's link TEXT; the dev build's link TARGET is the local
    preview server."""
    url = repo_https_url()
    if url is None:
        return None
    owner, repo = url[len("https://github.com/"):].split("/", 1)
    return f"https://{owner.lower()}.github.io/{repo}/week{week}/"


def submission_run(week, force=False):
    week_dir = f"week{week}"

    print(f"[1/5] Extracting {week_dir} plots + development report...")
    run_extract([week], force)

    print("[2/5] Rebuilding the dashboard...")
    build_dashboard()

    print("[3/5] Sweeping telemetry...")
    telemetry_status = sweep_telemetry(week)
    print(f"      {telemetry_status}")

    print("[4/5] Committing and pushing...")
    sha = commit_all(week)
    pushed = push_origin()
    print("push: origin updated" if pushed else "push: FAILED")

    # structural completeness — shown in the manifest AND driving the
    # warnings. Plot completeness is deliberately NOT adjudicated here:
    # students check their own week page in the preview.
    notebook_ok = (REPO_ROOT / week_dir / f"project{week}_solution.ipynb").exists()
    report_ok = (REPO_ROOT / week_dir / f"project{week}_development.md").exists()
    items, _ = scan_week(week)
    files_line = " · ".join([
        "solution notebook " + ("✅" if notebook_ok else "❌"),
        "development report " + ("✅" if report_ok else "❌"),
        f"plots: {len(items)}",
    ])

    local_url = dashboard_url(week)
    public_url = pages_url(week)
    dashboard_line = (f"[{public_url}]({public_url})" if public_url
                      else local_url)
    link = repo_commit_link(sha)
    version = f"[`{sha}`]({link})" if link else f"`{sha}`"
    pushed_line = ("yes" if pushed
                   else "**NO — the push failed; run `git push` from the "
                        "terminal and paste the manifest again**")

    manifest = (f"## Project {week}\n\n"
                f"- **Dashboard:** {dashboard_line}\n"
                f"- **Files:** {files_line}\n"
                f"- **Version:** {version}\n"
                f"- **Pushed:** {pushed_line}\n"
                f"- **Telemetry:** {telemetry_status}\n")

    print(f"[5/5] Writing {week_dir}/project{week}_manifest.md...")
    manifest_path = REPO_ROOT / week_dir / f"project{week}_manifest.md"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(manifest, encoding="utf-8")

    print()
    print(manifest)
    print(f"Open {week_dir}/project{week}_manifest.md in a markdown preview and "
          "paste the rendered manifest into the Canvas text-entry submission.")
    print(f"(local preview of your week page: {local_url})")
    ensure_server()

    warnings = []
    if not notebook_ok:
        msg = f"{week_dir}/project{week}_solution.ipynb is missing."
        if week == FIRST_WEEK:
            msg += (" (The week 2 notebook is ungraded, but submit it anyway"
                    " as a dry run of the full pipeline.)")
        warnings.append(msg)
    if not items:
        warnings.append(f"{week_dir}: no plots published — the week page is "
                        "empty or missing.")
    if not report_ok:
        warnings.append(f"{week_dir}/project{week}_development.md is missing "
                        "— the development report is part of every "
                        "submission.")
    if not pushed:
        warnings.append("git push failed — your work is committed and the "
                        "version above is valid, but your dashboard and the "
                        "pinned version are NOT published. Run `git push` "
                        "from the terminal (ask the agent for help), then "
                        "paste the manifest.")
    if warnings:
        print("\n" + "=" * 60)
        for w in warnings:
            print(f"WARNING: {w}\n")
        sys.exit(1)


# --------------------------------------------------------------------------

def run_extract(weeks, force):
    for week in weeks:
        plots = extract_plots(week, force=force)
        report = extract_report(week, force=force)
        plots_msg = {None: "no solution notebook"}.get(
            plots, plots if isinstance(plots, str) else f"{plots} images extracted")
        report_msg = "no development report" if report is None else report
        print(f"week{week}: plots: {plots_msg}; report: {report_msg}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("week", nargs="?", type=int,
                        help=f"project week ({FIRST_WEEK}-{LAST_WEEK})")
    parser.add_argument("--extract", action="store_true",
                        help="run extract_plots + extract_report, then stop")
    parser.add_argument("--build", action="store_true",
                        help="extract all weeks and rebuild the dashboard")
    parser.add_argument("--serve", action="store_true",
                        help="serve docs/ without rebuilding (the persistent "
                             "preview server; started at Codespace launch)")
    parser.add_argument("--force", action="store_true",
                        help="ignore freshness dates (repair/testing)")
    parser.add_argument("--port", type=int, default=8000,
                        help="preview server port (default 8000)")
    args = parser.parse_args()

    if args.week is not None and not FIRST_WEEK <= args.week <= LAST_WEEK:
        parser.error(f"week must be {FIRST_WEEK}-{LAST_WEEK}")

    if args.serve:
        serve(args.port)
        return

    if args.extract:
        weeks = [args.week] if args.week else range(FIRST_WEEK, LAST_WEEK + 1)
        run_extract(weeks, args.force)
        return

    if args.build:
        if args.week is not None:
            parser.error("--build covers every week; drop the week number")
        run_extract(range(FIRST_WEEK, LAST_WEEK + 1), args.force)
        build_dashboard()
        return

    if args.week is None:
        parser.error("give a week number, or --extract / --build / --serve")
    submission_run(args.week, args.force)


if __name__ == "__main__":
    main()
