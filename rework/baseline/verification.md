# Phase 7 — Verification Sweep & Exclusion Audit

Run 2026-09-15 against the local static server at the repository root, with
Chromium 153 driven headlessly. Every check below ran across **all thirteen**
styled pages listed in `inventory.md`, not a representative sample.

**Result: every check passes. No corrections to markup or styles were needed,
apart from adding the empty page-specific-overrides section noted under
"Consistency audit".**

## Per-page results

`scrollWidth <= innerWidth` at both widths; copy re-extracted and diffed against
`text/`; tag tree balanced; every internal reference resolving.

| Page | 380px | 1280px | Copy vs baseline | Tag balance |
|---|---|---|---|---|
| `/` | pass (380 ≤ 380) | pass (1280 ≤ 1280) | identical | balanced |
| `/docs/` | pass | pass | identical | balanced |
| `/docs/rounds/` | pass | pass | identical | balanced |
| `/docs/artifacts/` | pass | pass | identical | balanced |
| `/docs/settings/` | pass | pass | identical | balanced |
| `/docs/codescanner/` | pass | pass | identical | balanced |
| `/docs/brainstormer/` | pass | pass | identical | balanced |
| `/docs/agentifier/` | pass | pass | identical | balanced |
| `/docs/designer/` | pass | pass | identical | balanced |
| `/docs/stackadvisor/` | pass | pass | identical | balanced |
| `/docs/phaser/` | pass | pass | identical | balanced |
| `/docs/deployer/` | pass | pass | identical | balanced |
| `/bws4/` | pass | pass | identical | balanced |

No page failed the viewport check, so no overflow fix was required and no
`overflow-x: hidden` was reintroduced on `html`, `body` or `main`. The only two
rules in the stylesheet that declare overflow remain `.table-wrap` and `pre`.

## Audits

- **Tag balance.** `extract_text.py --check-balance` (added this phase; an
  `html.parser` subclass that pushes on start tags, pops on end tags and ignores
  the WHATWG void elements) reports a balanced tree on all thirteen. No tag
  closed out of order, none left open at EOF.
- **Link resolution.** 159 internal `href`/`src` references across the thirteen
  pages; every one resolves to a file present in the repository. Explicitly
  confirmed: `/styles.css`, both `.woff2` files, `favicon.svg`, `project.png`,
  `docs/settings/settings.png`, and all ten redirect-stub paths. Nothing was
  broken, so no reference needed fixing.
- **Copy byte-identity.** All thirteen diff empty against `text/`. Note that
  those baselines are the ones regenerated under amendment A5, derived from the
  untouched pre-round snapshots in `html/`.
- **Stub integrity.** `grep -rl 'http-equiv="refresh"' --include=index.html .`
  returns the **same ten paths** recorded in Phase 1 — `about/`,
  `how-it-works/`, and the eight under `agents/` including `reviewer/`. **None
  of the ten contains a stylesheet link, a font reference, a `<script>` or a
  `<style>`** (zero matches for all of those, in every one). Each is 13 lines.
  `git log` over `about/`, `how-it-works/` and `agents/` for the whole round
  returns no commits: not one stub was opened.
- **Dark-scheme audit.** All thirteen walked in both schemes. Every sampled
  colour — body background and text, muted text, code panel tint and text,
  figure caption, table rule, wordmark blue and green, nav link, current-section
  mark — differs between the two schemes on every page. **No colour failed to
  swap**, which is the mechanical form of "no literal escaped the tokens".
- **Contrast (SC 1.4.3, 4.5:1).** Measured from computed styles, not from source:

  | Pair | Light | Dark |
  |---|---|---|
  | primary text on background | 17.17:1 | 18.14:1 |
  | muted text on background | 6.72:1 | 7.67:1 |
  | code text on panel tint | 15.43:1 | 16.82:1 |
  | figure caption on background | 6.72:1 | 7.67:1 |

  All pass. The tightest pair is muted text in the light scheme at 6.72:1.
- **No-stylesheet readability.** `/`, `/docs/` and `/bws4/` loaded with the
  stylesheet request aborted — confirmed genuinely off (0 CSS rules applied,
  body falls back to Times, `main` runs full width). Each remains a readable
  plain document: exactly one `h1`, no heading level skipped, `NAV` then `MAIN`
  in source order, **zero elements carrying text that are hidden**, and all
  content present (17,961 / 6,660 / 5,484 characters). Every `<img>` carries a
  meaningful `alt`.
- **Exclusion audit.** `grep -niE
  'shadow|gradient|animation|transition|transform|@keyframes|border-radius'
  styles.css` returns **three matches, all `border-radius`**: `code` 2px, `pre`
  2px, and the `pre code` reset to 0. These are required by the design and are
  recorded as **amendment A4** — the design manifest and the `InstallCommand`
  surface both specify a 2px panel radius. Every other term in that grep returns
  nothing. `grep -rniE 'analytics|gtag|plausible|<svg|<script' --include=index.html .`
  returns **0 matches** across the whole repository.
- **Blue audit.** `--wordmark-blue` is consumed by **exactly one rule**,
  `.wordmark-spec`. (The token name appears three times in the file; the other
  two are its declarations in `:root` and the dark block.) `--accent-green` is
  consumed by **exactly three** — `.wordmark-four`, body links, and the
  current-section indicator — which is the expected count under **amendment
  A2**, not a defect.
- **Consistency audit.** Computed values are **identical across all thirteen
  pages**: prose stack (Charter first), 17px, 28.05px line-height, 27.2px `h1`,
  wordmark in JetBrains Mono 700, nav top at 0, and nav and prose sharing one
  left edge at 346px. Achieved entirely by the shared stylesheet: **0 inline
  `style` attributes, 0 `<style>` elements, and exactly one stylesheet loaded**
  (`/styles.css?v=6`) on every page. The `page-specific overrides` section was
  added this phase and is **intentionally empty**, with a comment stating that
  anything landing there must justify why it could not be shared.
- **Resource audit.** Every page requests exactly its own HTML, `/styles.css?v=6`,
  the two `.woff2` files, and its own images — four requests, or five on `/`
  (`project.png`) and `/docs/settings/` (`settings.png`). No request to any host
  other than the origin, and no 4xx, on any page.

## Copy drift carried forward

**None outstanding.** The Phase 6 check found no drift between any page and its
`rework/` copy file; the candidates it raised were each traced to artifacts of
the comparison and are written up under "Copy drift found" in `inventory.md`.
Nothing carries into a future round.

## Amendments in force

The five amendments recorded in `inventory.md` were all in force during this
sweep and are reflected in its expected values: A1 token names, A2 green as the
accent (three rules), A3 serif prose (register §8 amended to match), A4 the 2px
panel radius (three `border-radius` matches), A5 the regenerated text baselines.
