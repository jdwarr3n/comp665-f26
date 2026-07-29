# Week 2 — Development Report

> **This is a sample report.** It shows the kind of development report
> you will write each week: a short, honest account of how you and your
> AI agent produced the week's solution. Using the agent to help
> generate the report — including summarizing its own conversation —
> is fine. Reports are written in Markdown, a simple text format for
> documents like this one; if you haven't used Markdown before, ask
> the agent to write the report in Markdown and it will handle the
> formatting for you. This example shows development in Gemini chat
> and fixing one issue detected in the Codespace.
>
> Development reports should always be named `projectN_development.md`
> and saved in your `weekN/` directory. `preview_dashboard.sh`
> automatically converts them into HTML and saves them in `docs/` for
> display in your dashboard.

## How the work went

Saved the project description as an HTML file and downloaded
`project2_template.ipynb`, then attached both to a Gemini Pro chat and
asked for one code block per function in the template. Pasted the
blocks into `project2_solution.ipynb` in the Codespace and ran the
notebook in Jupyter.

The original Python code passed the week 2 machine grader on the first
`./build` run. However, while reviewing the solution images, we noted
that the histogram bins weren't centered at the integers as the project
description requires — matplotlib's default style centers bins
*between* the integers. Described the issue in the same Gemini
conversation and let Gemini fix the code; it passed explicit bin edges
offset by one half (`bins=[k - 0.5 for k in range(num_bins + 2)]`),
which matched the description on the next run.

Finished by re-running `./build` — the checker passed all tests and
pylint reported no style issues.

## Question answers

Project 2 has no required questions. When a project's template includes
required questions, answer them at the end of your report in this
format:

- **Question 1** The histogram narrows relative to its mean as n grows
  because the standard deviation grows as sqrt(n) while the mean grows
  as n.
