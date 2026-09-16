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

---

# Round amendments

Decisions taken during implementation that depart from what the phase files
say. The phase files under `.spec4/v1/phases/` are left exactly as Phaser wrote
them — they are the round's planning record, not a live document — so any
divergence is recorded here instead. Phase 7's audit should read this section
before it starts; its instruction 15 already requires carrying forward what is
noted here.

## A1 — Phase 2 tokens were renamed (Phase 3)

Phase 2 fixed the custom-property naming convention by example only
(`--color-bg`, `--font-mono`) and left the rest of the names to the
implementer. The names chosen at Phase 2 did not match the names Phases 3, 4, 5
and 7 go on to reference literally, so four were renamed in the Phase 3 commit:

| Phase 2 name | Current name | Referenced literally by |
|---|---|---|
| `--color-fg` | `--color-text` | phases 3, 4 |
| `--color-tint` | `--color-code-tint` | phases 3, 5 |
| `--color-blue` | `--wordmark-blue` | phases 4, 7 |
| `--color-green` | `--accent-green` | phase 4 |

Values and measured contrast ratios are unchanged; this was a rename only. It
is noted because the Phase 2 commit message and the styles.css history show the
older names, and anyone reading the Phase 2 record against the current file
would otherwise be puzzled. The three tokens no phase names literally —
`--measure`, `--font-size-base`, `--line-height-base` — keep their original
names.

## A2 — Green is restored as the accent for links and the nav indicator (Phase 4)

**Amends:** phase3.md instructions 7 and 8, and phase4.md instruction 11.

Phase 3 instruction 7 requires links to use `--color-text` with an underline and
forbids any link, heading or accent from using "the blue or green wordmark
tokens". Phase 4 instruction 11 likewise forbids green for the current-section
indicator. That is stricter than what the round actually decided, and it
contradicts the register, which governs every page:

- **§7 (Look):** "the app's green as the single accent" — green *is* the accent,
  and links are what an accent is for.
- **§17 (Not on any page):** "No second accent colour. No blue, except in the
  Spec4 wordmark, where it is the app's." — the wordmark-only restriction
  applies to **blue**, not to green.

The approved mock follows the register: it styles `a { color: var(--green) }`
and marks the current section with a green bottom rule. Phaser generalised the
blue rule onto green; the register and the mock are authoritative over the
generated phase text.

**What Phase 4 must do, in addition to its own instructions:**

1. Amend the `a` rule in the **base elements** section to
   `color: var(--accent-green)`, keeping the underline, thickness and
   underline-offset exactly as Phase 3 left them. Green carries the link
   colour; the underline still carries the affordance, so links remain
   distinguishable without colour.
2. Style `.site-nav a[aria-current="page"]` with the green bottom rule the mock
   uses (`border-bottom: 2px solid var(--accent-green)`), in place of phase4
   instruction 11's `--color-rule`. The indicator also raises the link to
   `--color-text`, so the current section is still marked by weight and a rule
   and not by colour alone.

Phase 4 therefore edits one rule inside the base-elements section. That is a
deliberate, recorded exception to the mandated section ordering, not scope
creep: the `a` rule belongs where Phase 3 put it and only its colour changes.

**Consequences for Phase 7's audit.** The colour audit should expect:

- **Blue** — exactly one rule, `.wordmark-spec`. Unchanged; the §17 guarantee
  and phase7 instruction 12 both still hold verbatim.
- **Green** — exactly three rules: the wordmark's `4` (`.wordmark-four`), body
  links (`a`), and the current-section indicator
  (`.site-nav a[aria-current="page"]`). A grep for `--accent-green` returning
  three references is the expected pass, not a failure.

Contrast for the green link colour is already measured and recorded beside the
token: 5.42:1 on the light background and 14.57:1 on the dark background, both
clearing SC 1.4.3's 4.5:1 for body text.

## A3 — The prose face is a serif, against register §8 (Phase 3, recorded retrospectively)

**Amends:** register §8.

Register §8 (Look) says "Sans-serif prose." The approved mock sets the body
face to `Charter, "Bitstream Charter", "Iowan Old Style", "Sitka Text",
Cambria, Georgia, serif`, and the Designer's `ReadingColumn` surface — carried
into every phase file — describes "a single ~70-character text column in **a
serif face**". Phases 2 and 3 were written to the mock, and the implementation
followed them, so `--font-prose` is a serif stack.

This is recorded rather than resolved. The design pass is later than the
register and is what was approved, so the serif stands; but §8 still reads
"sans-serif", and a future round's CodeScanner reading the register against the
stylesheet would otherwise flag it as a defect. Either the register should be
amended to match the design, or the decision revisited deliberately — not left
as a silent contradiction between two governing documents.

No other part of §8 is affected: the measure is ~70 characters as it requires
(73 at 1280px), and the layout is left-aligned.

**Resolved 2026-09-15.** Register §8 was amended to read "Serif prose — a
system stack, Charter first, Georgia fallback; no font files", with a dated
note recording that the design round settled it. The two governing documents
now agree and nothing is outstanding for a later round to rediscover.

## A4 — The code panel keeps its 2px radius (Phase 5)

**Amends:** phase5.md instruction 8 and its `border-radius` verification grep.

Phase 5 instruction 8 says to "remove any rounding, border, or shadow from the
panel — it is a flat tinted block", and the phase's verification runs
`grep -niE 'shadow|gradient|animation|transition|border-radius|counter-increment'`
expecting no matches. The design says otherwise, in the same phase file and in
the design manifest, twice:

- `InstallCommand` (a UI surface carried into every phase file, under the
  heading "These specifications are authoritative for this phase"):
  "Two-line install command in **a plain code panel (one tint, 2px radius,** no
  syntax colour, no line numbers)".
- `.spec4/v1/design/manifest.json`: "Code panel treatment (one tint, **2px
  radius**, horizontal scroll)".

The approved mock ships `border-radius: 2px` on both `pre` and inline `code`.
The conflict is internal to phase5.md — its authoritative specification section
contradicts its own instruction 8 — and the specification section wins, as that
section's own preamble states. Register §10 ("plain bordered panels; no window
chrome, no traffic-light dots, no titlebar") is about chrome, not corner radius,
and is satisfied either way.

The stylesheet therefore contains three `border-radius` declarations:

| Line | Rule | Value | Source |
|---|---|---|---|
| ~201 | `code` (inline) | `2px` | mock, shipped in Phase 3 |
| ~403 | `pre` | `2px` | mock and design manifest |
| ~414 | `pre code` | `0` | reset, so the inline treatment does not double-apply inside a panel |

**Consequence for Phase 7.** The `border-radius` term in Phase 5's grep is
expected to match these three lines and must not be treated as a failure. Every
other term in that grep — shadow, gradient, animation, transition,
counter-increment — still returns nothing, and those are the exclusions the
specification's success criteria actually name. Radius is not on the excluded
list in register §14 or §17.
