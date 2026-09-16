---
{
  "phase_number": 1,
  "total_phases": 7,
  "phase_title": "Baseline & Page Inventory — Integration Thread Over the Existing Site",
  "phase_summary": "Confirm the existing static site serves correctly as authored, mechanically classify every index.html in the repository into the thirteen styled pages and the ten meta-refresh redirect stubs, and capture a checked-in rendered-text baseline that every later phase diffs against. This phase writes no styles and changes no existing file.",
  "features": [],
  "capabilities": [],
  "tech_stack_spec": {
    "dependencies": [],
    "configurations": "No env vars, no build step, no package manager. Serve the repository root with any static file server already available on the machine (e.g. `python3 -m http.server 8000` from the repo root) purely for local viewing. The baseline capture script under rework/baseline/ uses only the Python 3 standard library, is never served, and adds no dependency to the site itself. Site hosting remains GitHub Pages over HTTPS via the existing CNAME; nothing is deployed during this round."
  },
  "instructions": [
    "Serve the repository root locally with a static file server and confirm the following pages load and render in a browser with their current styling: `/`, `/docs/`, and `/bws4/`. Do not modify any file to make this work — if a page fails to load, record the failure and its cause; do not fix it silently.",
    "From the repository root, run `grep -rl 'http-equiv=\"refresh\"' --include=index.html .` and capture the output verbatim. This is the authoritative classification mechanism for this round: the paths it returns are the redirect stubs, and every other index.html is a styled page.",
    "Verify that the grep returns exactly ten paths: `about/index.html`, `how-it-works/index.html`, and the eight pages under `agents/` (agentifier, brainstormer, codescanner, deployer, designer, phaser, reviewer, stackadvisor). If the count differs from ten, stop and report the discrepancy rather than proceeding.",
    "Run `find . -name index.html -not -path './examples/*'` and subtract the ten stub paths from the result. Verify the remainder is exactly thirteen paths: `index.html`, the eleven pages under `docs/` (the docs index plus rounds, artifacts, settings, codescanner, brainstormer, agentifier, designer, stackadvisor, phaser, deployer), and `bws4/index.html`. If the count differs from thirteen, stop and report the discrepancy.",
    "Create the new directory `rework/baseline/`. This is the single stated exception to the rule that `rework/` is untouched this round: you are adding a new subdirectory and must not alter, move, rename, or reformat any file that already exists under `rework/`.",
    "Write `rework/baseline/inventory.md` recording three lists under clear headings: the thirteen styled page paths, the ten redirect stub paths, and — for each of the thirteen — whether its current HTML contains a `<link rel=\"stylesheet\">` to styles.css and whether it contains any `<link>` or `@import` pointing at a host other than spec4.ai (note each such external host and the page it appears on, Google Fonts especially).",
    "Copy each of the thirteen styled pages' current HTML byte-for-byte into `rework/baseline/html/`, preserving the route path in the filename (e.g. `index.html`, `docs-rounds.html`, `bws4.html`). These are the pre-round snapshots used to prove copy byte-identity later.",
    "Write `rework/baseline/extract_text.py` using only the Python 3 standard library (html.parser). It must take an HTML file path, discard the contents of `<script>`, `<style>`, and `<head>`, emit the concatenated text nodes of the document body with runs of whitespace collapsed to single spaces and one text block per line, and print the result to stdout. It is a local verification aid only: it is never served, never referenced by any page, and adds no dependency to the site.",
    "Run `extract_text.py` over each of the thirteen snapshots in `rework/baseline/html/` and write the output to a matching `.txt` file under `rework/baseline/text/`. This is the authoritative rendered-text baseline for the whole round.",
    "Write `rework/baseline/README.md` in two short paragraphs: what the baseline is for (proving the rendered text of every page is byte-identical before and after this round, with the copy files under rework/ as the text source), and the exact command a later phase runs to re-extract and diff a page's text against its baseline.",
    "Record in `rework/baseline/inventory.md` the current byte size and a one-paragraph summary of what `styles.css` currently contains — specifically noting the presence of any `body { overflow-x: hidden }` rule and any hero, card, grid, or nav rule sets — so Phase 2 has a written record of what it is replacing.",
    "Commit `rework/baseline/` and nothing else. Confirm with `git status` that no file outside `rework/baseline/` has been created, modified, or deleted."
  ],
  "risk_assessment": {
    "potential_bottlenecks": "The code review of this repository read the ten redirect stubs as full pages because they carry the index.html filename and a <title>, so any instruction that trusts a prose description of the file tree rather than the repository itself will classify pages incorrectly and corrupt every later phase. A second bottleneck is the temptation to 'tidy' the existing styles.css or an existing rework/ file while in the neighbourhood, which would destroy the pre-round baseline this phase exists to capture.",
    "mitigation_strategy": "Classification is decided by the grep command's output and by nothing else, with an explicit expected count (ten stubs, thirteen styled pages) that halts the phase if reality disagrees. The phase ends with a `git status` assertion that no file outside the new rework/baseline/ directory was touched, which mechanically prevents incidental edits. The extension-less scratch file rework/temp and the self-contained artifacts under examples/ are excluded from every command in this phase and must not be read, edited, or built upon."
  },
  "verification": "Run `grep -rl 'http-equiv=\"refresh\"' --include=index.html .` from the repo root — expect exactly ten paths (about/, how-it-works/, and the eight under agents/ including reviewer/). Confirm `rework/baseline/inventory.md` lists exactly thirteen styled pages and ten stubs, that `rework/baseline/html/` contains thirteen snapshot files, and that `rework/baseline/text/` contains thirteen matching .txt files. Confirm `/`, `/docs/`, and `/bws4/` load in a browser from the local static server. Run `git status` and confirm every change is a new file under `rework/baseline/` — zero existing files modified or deleted.",
  "references": [
    {
      "standard": "WHATWG HTML Living Standard (meta http-equiv=refresh, used by the redirect stubs)",
      "url": "https://html.spec.whatwg.org/multipage/semantics.html#attr-meta-http-equiv-refresh"
    },
    {
      "standard": "GitHub Pages",
      "url": "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"
    },
    {
      "standard": "Python html.parser (standard library, used by the local baseline script)",
      "url": "https://docs.python.org/3/library/html.parser.html"
    }
  ]
}
---

# Phase 1 of 7: Baseline & Page Inventory — Integration Thread Over the Existing Site

Confirm the existing static site serves correctly as authored, mechanically classify every index.html in the repository into the thirteen styled pages and the ten meta-refresh redirect stubs, and capture a checked-in rendered-text baseline that every later phase diffs against. This phase writes no styles and changes no existing file.

## Tech Stack

**Configurations:** No env vars, no build step, no package manager. Serve the repository root with any static file server already available on the machine (e.g. `python3 -m http.server 8000` from the repo root) purely for local viewing. The baseline capture script under rework/baseline/ uses only the Python 3 standard library, is never served, and adds no dependency to the site itself. Site hosting remains GitHub Pages over HTTPS via the existing CNAME; nothing is deployed during this round.

## Instructions

1. Serve the repository root locally with a static file server and confirm the following pages load and render in a browser with their current styling: `/`, `/docs/`, and `/bws4/`. Do not modify any file to make this work — if a page fails to load, record the failure and its cause; do not fix it silently.
2. From the repository root, run `grep -rl 'http-equiv="refresh"' --include=index.html .` and capture the output verbatim. This is the authoritative classification mechanism for this round: the paths it returns are the redirect stubs, and every other index.html is a styled page.
3. Verify that the grep returns exactly ten paths: `about/index.html`, `how-it-works/index.html`, and the eight pages under `agents/` (agentifier, brainstormer, codescanner, deployer, designer, phaser, reviewer, stackadvisor). If the count differs from ten, stop and report the discrepancy rather than proceeding.
4. Run `find . -name index.html -not -path './examples/*'` and subtract the ten stub paths from the result. Verify the remainder is exactly thirteen paths: `index.html`, the eleven pages under `docs/` (the docs index plus rounds, artifacts, settings, codescanner, brainstormer, agentifier, designer, stackadvisor, phaser, deployer), and `bws4/index.html`. If the count differs from thirteen, stop and report the discrepancy.
5. Create the new directory `rework/baseline/`. This is the single stated exception to the rule that `rework/` is untouched this round: you are adding a new subdirectory and must not alter, move, rename, or reformat any file that already exists under `rework/`.
6. Write `rework/baseline/inventory.md` recording three lists under clear headings: the thirteen styled page paths, the ten redirect stub paths, and — for each of the thirteen — whether its current HTML contains a `<link rel="stylesheet">` to styles.css and whether it contains any `<link>` or `@import` pointing at a host other than spec4.ai (note each such external host and the page it appears on, Google Fonts especially).
7. Copy each of the thirteen styled pages' current HTML byte-for-byte into `rework/baseline/html/`, preserving the route path in the filename (e.g. `index.html`, `docs-rounds.html`, `bws4.html`). These are the pre-round snapshots used to prove copy byte-identity later.
8. Write `rework/baseline/extract_text.py` using only the Python 3 standard library (html.parser). It must take an HTML file path, discard the contents of `<script>`, `<style>`, and `<head>`, emit the concatenated text nodes of the document body with runs of whitespace collapsed to single spaces and one text block per line, and print the result to stdout. It is a local verification aid only: it is never served, never referenced by any page, and adds no dependency to the site.
9. Run `extract_text.py` over each of the thirteen snapshots in `rework/baseline/html/` and write the output to a matching `.txt` file under `rework/baseline/text/`. This is the authoritative rendered-text baseline for the whole round.
10. Write `rework/baseline/README.md` in two short paragraphs: what the baseline is for (proving the rendered text of every page is byte-identical before and after this round, with the copy files under rework/ as the text source), and the exact command a later phase runs to re-extract and diff a page's text against its baseline.
11. Record in `rework/baseline/inventory.md` the current byte size and a one-paragraph summary of what `styles.css` currently contains — specifically noting the presence of any `body { overflow-x: hidden }` rule and any hero, card, grid, or nav rule sets — so Phase 2 has a written record of what it is replacing.
12. Commit `rework/baseline/` and nothing else. Confirm with `git status` that no file outside `rework/baseline/` has been created, modified, or deleted.

## Risk Assessment

**Potential bottlenecks:**

The code review of this repository read the ten redirect stubs as full pages because they carry the index.html filename and a <title>, so any instruction that trusts a prose description of the file tree rather than the repository itself will classify pages incorrectly and corrupt every later phase. A second bottleneck is the temptation to 'tidy' the existing styles.css or an existing rework/ file while in the neighbourhood, which would destroy the pre-round baseline this phase exists to capture.

**Mitigation strategy:**

Classification is decided by the grep command's output and by nothing else, with an explicit expected count (ten stubs, thirteen styled pages) that halts the phase if reality disagrees. The phase ends with a `git status` assertion that no file outside the new rework/baseline/ directory was touched, which mechanically prevents incidental edits. The extension-less scratch file rework/temp and the self-contained artifacts under examples/ are excluded from every command in this phase and must not be read, edited, or built upon.

## Verification

Run `grep -rl 'http-equiv="refresh"' --include=index.html .` from the repo root — expect exactly ten paths (about/, how-it-works/, and the eight under agents/ including reviewer/). Confirm `rework/baseline/inventory.md` lists exactly thirteen styled pages and ten stubs, that `rework/baseline/html/` contains thirteen snapshot files, and that `rework/baseline/text/` contains thirteen matching .txt files. Confirm `/`, `/docs/`, and `/bws4/` load in a browser from the local static server. Run `git status` and confirm every change is a new file under `rework/baseline/` — zero existing files modified or deleted.

## References

- [WHATWG HTML Living Standard (meta http-equiv=refresh, used by the redirect stubs)](https://html.spec.whatwg.org/multipage/semantics.html#attr-meta-http-equiv-refresh)
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Python html.parser (standard library, used by the local baseline script)](https://docs.python.org/3/library/html.parser.html)
