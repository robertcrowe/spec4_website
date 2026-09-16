# Phase 1 Baseline Inventory

Captured 2026-09-15 from the repository as authored, before any Phase 2+ change.
Classification was decided mechanically, by command output only:

```
grep -rl 'http-equiv="refresh"' --include=index.html .    # -> the 10 redirect stubs
find . -name index.html -not -path './examples/*'          # -> 23 total; 23 - 10 = 13 styled pages
```

Both counts matched the expected values exactly (10 stubs, 13 styled pages), so
the phase proceeded.

`examples/` is excluded from every command here, and the extension-less scratch
file `rework/temp` was not read or touched.

## Styled pages (13)

| # | Route | Source path | Baseline snapshot |
|---|-------|-------------|-------------------|
| 1 | `/` | `index.html` | `html/index.html` |
| 2 | `/docs/` | `docs/index.html` | `html/docs-index.html` |
| 3 | `/docs/rounds/` | `docs/rounds/index.html` | `html/docs-rounds.html` |
| 4 | `/docs/artifacts/` | `docs/artifacts/index.html` | `html/docs-artifacts.html` |
| 5 | `/docs/settings/` | `docs/settings/index.html` | `html/docs-settings.html` |
| 6 | `/docs/codescanner/` | `docs/codescanner/index.html` | `html/docs-codescanner.html` |
| 7 | `/docs/brainstormer/` | `docs/brainstormer/index.html` | `html/docs-brainstormer.html` |
| 8 | `/docs/agentifier/` | `docs/agentifier/index.html` | `html/docs-agentifier.html` |
| 9 | `/docs/designer/` | `docs/designer/index.html` | `html/docs-designer.html` |
| 10 | `/docs/stackadvisor/` | `docs/stackadvisor/index.html` | `html/docs-stackadvisor.html` |
| 11 | `/docs/phaser/` | `docs/phaser/index.html` | `html/docs-phaser.html` |
| 12 | `/docs/deployer/` | `docs/deployer/index.html` | `html/docs-deployer.html` |
| 13 | `/bws4/` | `bws4/index.html` | `html/bws4.html` |

Snapshot filenames intentionally mirror the existing `rework/*.md` copy-file
names (`docs-index`, `docs-rounds`, `bws4`, …) so a page's copy, snapshot, and
text baseline line up by stem. The one divergence is the front page: its copy
file is `rework/front-page.md` while its snapshot is `html/index.html`.

## Redirect stubs (10)

These carry an `index.html` filename and a `<title>`, but their entire body is a
`<meta http-equiv="refresh">` bounce. They are **not** pages and must not be
styled, rewritten, or counted as content in any later phase.

1. `about/index.html`
2. `how-it-works/index.html`
3. `agents/agentifier/index.html`
4. `agents/brainstormer/index.html`
5. `agents/codescanner/index.html`
6. `agents/deployer/index.html`
7. `agents/designer/index.html`
8. `agents/phaser/index.html`
9. `agents/reviewer/index.html`
10. `agents/stackadvisor/index.html`

Note that `agents/reviewer/` is a stub with no styled counterpart anywhere in
the repository — there is no `docs/reviewer/`.

## Stylesheet and external-host audit (the 13 styled pages)

Every one of the thirteen links `styles.css` with a `?v=5` cache-buster, at a
depth-appropriate relative path. No page uses `@import` anywhere. The only
non-`spec4.ai` hosts referenced from a `<link>` tag are the two Google Fonts
hosts, and they appear on all thirteen pages identically.

| Route | `<link rel="stylesheet">` to styles.css | `@import` | External hosts in `<link>` |
|-------|------------------------------------------|-----------|-----------------------------|
| `/` | yes — `styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/` | yes — `../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/rounds/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/artifacts/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/settings/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/codescanner/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/brainstormer/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/agentifier/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/designer/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/stackadvisor/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/phaser/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/docs/deployer/` | yes — `../../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |
| `/bws4/` | yes — `../styles.css?v=5` | none | fonts.googleapis.com, fonts.gstatic.com |

The Google Fonts dependency on every page is three tags: `preconnect` to
`fonts.googleapis.com`, `preconnect` to `fonts.gstatic.com` (crossorigin), and a
stylesheet `href` for `Inter:wght@400;500;600;700` plus
`JetBrains+Mono:wght@400;500;600;700` with `display=swap`. Those two families are
what `--font-sans` and `--font-mono` in `styles.css` name first, so removing the
Google Fonts link without replacing the faces would silently change every page's
typography.

Other external hosts do appear on some pages, but only in ordinary anchor
`href`s, never in a `<link>` or `@import`: `github.com` (all thirteen),
`exa.ai` and `tavily.com` (`/`, `/docs/`, `/docs/settings/`), `docs.astral.sh`
(`/`, `/docs/`), and `kriterion.ai` (`/` only).

## styles.css as it stands before Phase 2

**Size: 38,006 bytes, 1,178 lines.** Single stylesheet, hand-authored, no build
step, no minification, served from the repository root and shared by all
thirteen pages.

It opens with a `:root` custom-property block defining the whole design
language: a blue primary ramp (`#1E88E5` with light/dark variants), a
high-saturation green accent (`#39FF14`), a near-black dark-mode-only surface
ramp (`--color-background: #0a0a0f` through `--color-surface-elevated`), three
text tints, two blueprint grid-line colors, the `Inter`/`JetBrains Mono` font
stacks, an eight-step spacing scale, four radii, two transition durations, and
`--nav-height: 64px`. There is no light-mode palette and no
`prefers-color-scheme` block anywhere — the site is dark-only by construction.
After that comes a small reset in which **`body` does carry
`overflow-x: hidden`** (line 49, in the same declaration as the font, color and
background) — the rule Phase 2 needs to be deliberate about, since it is
currently masking rather than preventing horizontal overflow. Two other
`overflow-x` declarations exist and are unrelated scroll containers: `auto` on a
code/table wrapper at line 760 and on `.table-wrap` inside the responsive block
at line 1160.

The remainder is roughly forty comment-delimited rule sets, in source order:
blueprint grid background; navigation (the nav bar, a dropdown at line 99, and a
mobile menu at line 177); buttons; shared layout containers; the landing hero at
line 256 with its pipeline diagram; demo-video, problem, and pipeline-bar
sections; landing agent cards at line 454; terminal quote; a separate non-landing
page hero at line 570 and an agent-page hero at line 590; content sections; the
How-It-Works steps layout; screenshot frame; JSON code blocks; conversation
block; area cards; in-content link styling; StackAdvisor covers list; output
label; use cases; getting started; Phaser principle cards and output flow; the
About pipeline table; the Agentifier tier ladder; the About for-list; CTA
section; the BWS4 section at line 1055; footer; a fade-in animation; and a single
responsive block beginning at line 1114 that carries all the breakpoint
overrides. Hero rules, card rules, grid rules (23 `display: grid` /
`grid-template` declarations) and nav rules are therefore not centralized — they
are scattered per-section and per-page, which is what makes a wholesale
replacement in Phase 2 higher-risk than the line count suggests.
