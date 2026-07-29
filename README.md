# COMP 665 — Data Visualization

Course repository for **COMP 665 (Data Visualization)**. Each week's project
lives in its own folder, and everything runs in a preconfigured GitHub
Codespace — no local Python setup required.

## Getting started

1. Create your own copy of this repository — the **GitHub** page on
   Canvas walks you through it.
2. Open **your copy** in a **GitHub Codespace** (green "Code" button →
   Codespaces). The container provides the frozen course environment
   (Python 3.10 + the Jupyter notebook server — the classic view you
   see in the class videos).
3. From the terminal, run `./update_course.sh` once — it connects your
   copy to the course repo and pulls any course updates newer than your
   copy. Run it again whenever the instructor announces an update.
4. Verify your environment by running `version-verifier310.ipynb` — it checks
   that every package matches the versions the machine grader expects.

## Weekly workflow

The **Codespaces** and **Agents** pages on Canvas cover this flow in
detail — the recommended way to develop each solution is Gemini Pro
chat (attach the project description and template; see the Agents
page), with the Codespace as the place you run, test, and submit.

1. Create your working notebook from the week's template:

   ```bash
   cd weekN
   cp projectN_template.ipynb projectN_solution.ipynb
   ```

   (Simple file operations like this can also be done in the Explorer
   pane — right-click a file for **Copy**, **Paste**, and **Rename**.)

2. Open the Jupyter notebook server — from the repo's top level run
   `./start_jupyter.sh`. The server starts with the Codespace; this
   opens it in a browser tab (restarting it first if needed). If no
   tab appears: run it again, or click the world icon on the port
   labeled **"Jupyter"** in the Ports tab. Run `projectN_solution.ipynb`
   there, top to bottom, so the solution images
   are saved in the notebook — peers review those plots. Jupyter
   auto-saves every two minutes, but save manually before closing.
   Your plots also feed your public **dashboard**: embedded figures are
   extracted automatically, and the weeks that write files (animations,
   interactive HTML) save directly into `docs/weekN/plots/`.
3. Check your work by running the machine grader locally:

   ```bash
   ./build
   ```

   This converts your `projectN_solution.ipynb` to a script, runs the
   project's checker (`projectN_checker.py`), and then the style
   checker. When it reports a problem, paste the output into your
   Gemini conversation and let it suggest a fix. Also check your
   generated images against the project description — the grader
   passing does not mean the plots are right, and the submitted images
   are your responsibility.
4. Write your **development report** — `weekN/projectN_development.md`,
   in Markdown — a short, honest account of how you and your agent
   produced the solution, plus answers to any questions in the
   notebook. It appears on your dashboard's week page, where peers
   review it. A sample report is on your dashboard's Week 2 page.

## Your dashboard

Every repo publishes a portfolio dashboard built from your weekly plots
and development reports. Two commands, from the repo's top level:

```bash
./start_dashboard.sh     # open the dashboard in a browser tab
./rebuild_dashboard.sh   # rebuild it from your weekN/ work, then refresh the tab
```

The preview server runs from Codespace launch, so `start_dashboard`
normally just opens the tab (if no tab appears: run it again, or click
the world icon on the **"Dashboard preview"** port in the Ports tab).
The tab always shows the dashboard **as of the last rebuild** — after
new work, run `rebuild_dashboard` and refresh.
The preview is local and private. Serving your dashboard publicly is
optional — see the **GitHub** page on Canvas.
**Never edit files under `docs/` by hand** — everything there is
generated; you author your work in `weekN/`.

## Submitting on Canvas

> **Fall 2026 beta:** this section is **not operational** — Vocareum
> remains the official submission method for F26. Beta testers are
> welcome to run `make_manifest.py` and look at the manifest it
> produces, but nothing here counts as a submission.

When your week is done — notebook **saved**, development report
written, dashboard checked in the preview — run:

```bash
python3 make_manifest.py N
```

It rebuilds your dashboard, commits and pushes your work (publishing
your public dashboard), and writes `weekN/projectN_manifest.md`. Open that file in a **markdown preview**
(right-click it in the explorer → **Open Preview**) and paste the
rendered manifest (links intact) into the Canvas text-entry
submission. Running the script does not submit anything — the Canvas
paste is the submission.

*(Telemetry is stubbed in the current build — the manifest's Telemetry
line reports "skipped".)*

## Repository layout

| Path | Contents |
|---|---|
| `weekN/projectN_template.ipynb` | Starting notebook for the week's project |
| `weekN/projectN_checker.py`, `weekN/build` | The machine grader and the script that runs it |
| `weekN/data/` | Project input data and test files |
| `weekN/examples/` | Worked examples and templates used in class |
| `weekN/projectN_development.md` | Your weekly development report (rendered on the dashboard) |
| `docs/` | Your generated dashboard — never hand-edited; plots land in `docs/weekN/plots/` |
| `public/` | Shared grader support files (style checker configuration) |
| `make_manifest.py` | Builds the dashboard, pushes your work, and writes each week's Canvas submission manifest |
| `start_jupyter.sh` | Open the Jupyter notebook server in a browser tab |
| `start_dashboard.sh` | Open your dashboard in a browser tab |
| `rebuild_dashboard.sh` | Rebuild the dashboard from your `weekN/` work |
| `update_course.sh` | Pull the latest course files into your copy of the repo |
| `requirements310.txt`, `.devcontainer/` | The frozen course environment |

## Rules of the road

- Don't edit the checkers, `public/`, `data/`, or the environment files —
  the grader depends on them exactly as they are.
- **Push after each development session** — the Codespace is only a
  working copy; your repo is the permanent store.
- **When the instructor announces a course update**, run
  `./update_course.sh` from the repo's top level — it pulls the latest
  course files (checkers, scripts, templates) into your copy without
  touching your work.
- **Keep ONE Codespace, and delete stale ones** — beta testing runs on
  your personal GitHub quota, and every stopped Codespace holds on to
  several GB of it. Stop (don't delete) the one you're using; pushed
  work is always safe to recreate from. Use the default 2-core machine.
  If prompted to rebuild the container, push first — committed work
  survives a rebuild.
- **Don't install packages.** The container has everything the projects
  need; code that depends on extra packages will fail the official
  machine grader (run by the instructor after peer review completes).
