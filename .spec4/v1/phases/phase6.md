---
{
  "phase_number": 6,
  "total_phases": 7,
  "phase_title": "Propagation Across All Thirteen Pages",
  "phase_summary": "The round's only markup phase: apply the identical head → nav → main skeleton to all thirteen styled pages, add the minimum markup the stylesheet needs, remove the Google Fonts link from every page, and leave the rendered copy byte-identical and the ten redirect stubs untouched.",
  "features": [
    {
      "id": "unified_stylesheet",
      "role": "extended",
      "scope_note": "Applies the completed stylesheet and its markup contracts to all thirteen styled pages; the cross-page verification sweep and exclusion audit land in Phase 7."
    }
  ],
  "capabilities": [],
  "tech_stack_spec": {
    "dependencies": [],
    "configurations": "Edits the thirteen styled page HTML files identified in rework/baseline/inventory.md, plus no other file. HTML is 2-space indented with double-quoted attributes; classes and ids are kebab-case. Every page links the single root-relative /styles.css and no other stylesheet. Self-hosted fonts are served from fonts/; no external host is referenced. The ten redirect stubs under about/, how-it-works/, and agents/ are not opened for editing."
  },
  "instructions": [
    "Read rework/baseline/inventory.md and work only through the thirteen styled page paths it lists. Do not open, edit, or reformat any of the ten redirect stubs, any file under examples/, or any existing file under rework/.",
    "Reference .spec4/v1/design/mock.html for the intended visual result as you apply the skeleton. It is a look reference only: its front page rewrote the site's headings, its screenshot is hand-drawn HTML with invented figures, and its `<script>` and `main { display: none }` exist solely to hold three pages in one file. None of that is built, and no character of the mock's copy enters any page.",
    "For each of the thirteen pages, establish the identical skeleton: `<head>` → `<nav>` → `<main>`, with no footer. Do not add a `<footer>` element to any page — the nav carries the version, and every fact the mock's footer line held is already present on the front page's trust strip.",
    "In each page's `<head>`, ensure exactly these elements are present and correct: charset utf-8, `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">`, the page title, the existing description and Open Graph tags preserved as they are, the favicon link, and a single `<link rel=\"stylesheet\" href=\"/styles.css\">`. Preserve the existing canonical and social metadata values verbatim — do not rewrite titles, descriptions, or OG values.",
    "Remove the Google Fonts `<link>` elements from every one of the thirteen pages — including any `<link rel=\"preconnect\">` to fonts.googleapis.com or fonts.gstatic.com and any `@import` of a Google Fonts URL. After this phase no page requests a byte from any host other than spec4.ai; the JetBrains Mono weights are served from fonts/ by the Phase 2 @font-face rules.",
    "Delete any remaining `<style>` block and any `style=\"...\"` attribute from the thirteen pages, so the shared stylesheet is the single source of presentation for the whole site.",
    "Replace each page's existing nav with the canonical nav markup contract recorded as a comment at the top of the nav section of styles.css, copied identically onto every page — same elements, same classes, same order, same three links.",
    "Set the current-section mark per the contract: `aria-current=\"page\"` on the Docs link for the docs index and all ten docs pages, `aria-current=\"page\"` on the Examples link for bws4/index.html, and no aria-current at all on index.html. Do not add a Home link to index.html or to any other page.",
    "Wrap every `<table>` on every page in a `<div class=\"table-wrap\">` per the components markup contract. Add the wrapper only — do not reorder columns, merge cells, change header text, or alter any cell content.",
    "Confirm every code block on every page is a `<pre><code>` pair, and strip any leftover syntax-highlighting spans, language classes, or line-number markup from inside them. Removing a highlighting span must not change the characters of the code text itself.",
    "Confirm every figure on every page is a `<figure>` containing an `<img>` with a meaningful `alt` followed by a `<figcaption>`, per the components markup contract. If an existing image already carries caption text in a sibling paragraph, move that exact text into the figcaption without rewording it.",
    "Remove every class, id, and wrapper element left over from the previous stylesheet that the new stylesheet does not use — hero, card, grid, and container classes in particular. Remove the wrapper element only where doing so changes no text; where a wrapper carries text, strip its class and leave the element.",
    "Verify the rendered text of each page against its authoritative copy file under rework/ — the copy files are the text source, and this round changes styles.css and the minimum markup the stylesheet needs, nothing else. If a page's text and its copy file disagree, do not resolve it here: record the discrepancy in rework/baseline/inventory.md under a 'copy drift found' heading and leave the page's text exactly as it is.",
    "After editing each page, re-extract its text with rework/baseline/extract_text.py and diff against its file in rework/baseline/text/. The diff must be empty. If it is not, your markup edit changed the copy — revert that edit and redo it structurally.",
    "Confirm no page loads any resource except its own HTML, /styles.css, the two self-hosted fonts, and its own images. Add no script tag, no analytics snippet, and no third-party embed to any page."
  ],
  "risk_assessment": {
    "potential_bottlenecks": "Thirteen files edited by hand is where drift enters: a nav copied with a typo onto page seven, a stray class kept on page eleven 'because it looked needed', an aria-current left on the front page. The sharper risk is copy damage — unwrapping a leftover container div or stripping a highlighting span is exactly the kind of edit that silently swallows a text node, and a missing word is invisible to visual inspection across thirteen pages. A third risk is an agent treating the mock as a content source and rewriting a heading to match it.",
    "mitigation_strategy": "The nav and the three components are applied from markup contracts that live as comments inside styles.css itself, so all thirteen pages copy one written structure rather than each being re-derived. Copy damage is caught mechanically rather than visually: every page is re-extracted with the Phase 1 script and diffed against its baseline immediately after editing, and a non-empty diff means the edit is reverted and redone — the baseline exists precisely because this phase runs in a fresh session with no memory of the original text. The mock's status as a look-only reference is stated in the instructions, and the byte-identity diff would catch any copy borrowed from it. Copy drift discovered against the rework/ files is recorded rather than fixed, keeping this round's change confined to presentation."
  },
  "verification": "Run `grep -rniE 'fonts\\.googleapis|fonts\\.gstatic|@import' --include=index.html .` and expect no matches: no `<link>` or `@import` to any host other than spec4.ai exists on any of the thirteen pages. Run `grep -rn '<script' --include=index.html .` and expect no matches, satisfying nfr_every_page_loads_and_renders_correctly_without_requiring_any_script_to_run. Run `grep -rn '<footer' --include=index.html .` and expect no matches on the thirteen styled pages. Run `grep -rc 'styles.css' --include=index.html .` and confirm each of the thirteen pages links it exactly once and each of the ten stubs links it zero times. Run `grep -rn 'aria-current' --include=index.html .` and confirm exactly twelve matches — the docs index, the ten docs pages, and bws4 — with none on index.html. Confirm every `<table>` in the thirteen pages is preceded by a `<div class=\"table-wrap\">`. Re-extract all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, proving the rendered copy is byte-identical before and after. Load each page from the local server with the Network panel open and confirm the only requests are the page, /styles.css, the two .woff2 files, and that page's own images, satisfying nfr_pages_load_quickly_even_on_slow_connections__given_they_contain_no_scripts__media_playback__or_heavy_assets and nfr_the_site_collects_no_analytics_or_tracking_information_about_readers.",
  "references": [
    {
      "standard": "WHATWG HTML Living Standard",
      "url": "https://html.spec.whatwg.org/multipage/"
    },
    {
      "standard": "WHATWG HTML Living Standard (meta http-equiv=refresh, used by the redirect stubs)",
      "url": "https://html.spec.whatwg.org/multipage/semantics.html#attr-meta-http-equiv-refresh"
    },
    {
      "standard": "Open Graph protocol",
      "url": "https://ogp.me"
    },
    {
      "standard": "ARIA aria-current attribute",
      "url": "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-current"
    },
    {
      "standard": "GitHub Pages",
      "url": "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"
    }
  ]
}
---

# Phase 6 of 7: Propagation Across All Thirteen Pages

The round's only markup phase: apply the identical head → nav → main skeleton to all thirteen styled pages, add the minimum markup the stylesheet needs, remove the Google Fonts link from every page, and leave the rendered copy byte-identical and the ten redirect stubs untouched.

## Feature Specifications

These specifications are authoritative for this phase. Implement to them; the instructions below tell you how and in what order.

### Unified_Stylesheet — product feature — extended in this phase

*Scope for this phase: Applies the completed stylesheet and its markup contracts to all thirteen styled pages; the cross-page verification sweep and exclusion audit land in Phase 7.*

Gives every page of the site one consistent visual presentation so the site reads as a single coherent reference work rather than a marketing site, while sharing a few brand cues with the Spec4 app.

**Invocation**

- Trigger: A reader opens or navigates to any page on the site

**Inputs**

- `page content` (structured text, required) — The prose, code samples, tables, figures, and navigation links that make up a given page
- `system color scheme preference` (setting, optional) — The reader's device-level preference for a light or dark reading scheme
- `viewport width` (measurement, optional) — The width of the reader's window or screen, used to decide when wide content needs to scroll
- `current section identifier` (text, required) — Which of the three main sections the current page belongs to, so navigation can mark it as active

**Outputs**

- Primary: A visually consistent rendering of the page
- Format: visual page layout
- Schema notes: Every page shows the same wordmark, navigation, typography choices, table behavior, code presentation, figure treatment, and color scheme rules; only content differs between pages

**Success criteria**

- All thirteen pages share identical navigation placement, wordmark treatment, and typography choices
- The wordmark's two-color treatment is the only place blue appears on the site
- Switching a device between light and dark reading preference changes the site's appearance without any control on the page
- Wide tables and code samples scroll within their own bounded area instead of breaking the page layout on narrow screens
- Figures appear at a consistent full-column width with a visible caption
- The active section is visibly indicated in the navigation on every page in that section
- No icons, card shapes, hero banners, shadows, gradients, animation, a second accent color, or analytics indicators appear anywhere on the site

**Failure modes**

- One or more pages render with different typography, spacing, or navigation than the rest (likelihood: medium) — mitigation: Apply the same shared presentation rules to every page rather than page-specific overrides
- Dark reading scheme produces low-contrast or unreadable text (likelihood: medium) — mitigation: Define paired light and dark colors for background and text that both meet clear readability at normal reading distance
- A wide table or long code sample overflows and breaks the page layout on a narrow screen (likelihood: medium) — mitigation: Contain such content in a bounded, independently scrollable area
- A visible control for switching color scheme appears, contradicting the no-toggle guarantee (likelihood: low) — mitigation: Drive the scheme purely from the reader's system-level preference with no on-page control
- Excluded decorative elements (icons, shadows, gradients, animation, extra accent color, analytics) creep back in over time (likelihood: low) — mitigation: Treat the exclusion list as a standing constraint checked whenever the shared presentation is changed

- entities: Page, Section, Navigation, Figure, Table, CodeSample, ColorScheme

### UI surfaces for this phase (from the design)

- **`SiteNav`** [non_ai]
  - screens: front
  - inputs: section links: Docs, Examples, GitHub
  - output: One-line nav: two-colour wordmark (Spec blue, 4 green), version 1.5.0 in monospace, three text links; the current section carries a short green rule; identical on every page
  - states: front (no section active), docs active, examples active, narrow (wraps, no horizontal breakage), light, dark
  - reads: Navigation, Section, ColorScheme
- **`ReadingColumn`** [non_ai]
  - screens: front
  - output: A single ~70-character text column in a serif face with generous line-height; headings in the same face at a larger size; system colour scheme applied with no toggle
  - states: light, dark, narrow
  - reads: Page, ColorScheme
  - after (advisory UI ordering): SiteNav
- **`InstallCommand`** [non_ai]
  - screens: front
  - output: Two-line install command in a plain code panel (one tint, 2px radius, no syntax colour, no line numbers), followed by a version/licence line
  - states: default, long line scrolls within panel
  - reads: CodeSample
  - after (advisory UI ordering): ReadingColumn
- **`ProjectPageFigure`** [non_ai]
  - screens: front
  - output: Full-column-width figure of the app's project page on Spec4's own repository with an italic caption below
  - states: default, narrow (scales to column)
  - reads: Figure
  - after (advisory UI ordering): ReadingColumn
- **`ArtifactTree`** [non_ai]
  - screens: front
  - output: The .spec4/v1/ file tree in a code panel with a per-file comment naming the agent that writes it
  - states: default, wide lines scroll within panel
  - reads: CodeSample, ArtifactFile
  - after (advisory UI ordering): ReadingColumn
- **`PhaseExcerpt`** [non_ai]
  - screens: front
  - output: A long Markdown excerpt of .spec4/v0/phases/phase1.md in a code panel — the thing a coding agent is handed
  - states: default, wide lines scroll within panel
  - reads: CodeSample
  - after (advisory UI ordering): ReadingColumn
- **`AgentTable`** [non_ai]
  - screens: front
  - output: Four-column table — Agent, Reads, Writes, Runs — header row distinguished by weight and a rule, no fill; scrolls horizontally inside its wrapper on narrow screens
  - states: default, narrow (wrapper scrolls)
  - reads: Table, Agent
  - after (advisory UI ordering): ReadingColumn
- **`SiteFooter`** [non_ai]
  - screens: front
  - output: One plain line above a rule: version, licence, source, no analytics
  - states: default
  - reads: Navigation
  - after (advisory UI ordering): ReadingColumn
- **`DocsInstall`** [non_ai]
  - screens: docs
  - output: Install from PyPI and from source, two code panels, plus the upgrade line
  - states: default
  - reads: CodeSample
  - after (advisory UI ordering): ReadingColumn
- **`RoundTable`** [non_ai]
  - screens: docs
  - output: Agent / Reads / Writes table for the seven agents in a scrolling wrapper
  - states: default, narrow (wrapper scrolls)
  - reads: Table, Agent
  - after (advisory UI ordering): ReadingColumn
- **`ButtonTable`** [non_ai]
  - screens: docs
  - output: Button / Meaning table: Start, Continue, Modify, Needs Update, Not Ready, Required
  - states: default
  - reads: Table
  - after (advisory UI ordering): ReadingColumn
- **`AppsTable`** [non_ai]
  - screens: examples
  - output: App / Tier / Round table of the nine gallery apps
  - states: default
  - reads: Table, ExampleApp
  - after (advisory UI ordering): ReadingColumn
- **`RoundsTable`** [non_ai]
  - screens: examples
  - output: Round / What it planned / Agents run table for v0–v8 in a scrolling wrapper
  - states: default, narrow (wrapper scrolls)
  - reads: Table, Round
  - after (advisory UI ordering): ReadingColumn
- **`CatalogExcerpt`** [non_ai]
  - screens: examples
  - output: ai_catalog.json excerpt showing recommendation and decision side by side, in a code panel
  - states: default, wide lines scroll within panel
  - reads: CodeSample
  - after (advisory UI ordering): ReadingColumn

## Tech Stack

**Configurations:** Edits the thirteen styled page HTML files identified in rework/baseline/inventory.md, plus no other file. HTML is 2-space indented with double-quoted attributes; classes and ids are kebab-case. Every page links the single root-relative /styles.css and no other stylesheet. Self-hosted fonts are served from fonts/; no external host is referenced. The ten redirect stubs under about/, how-it-works/, and agents/ are not opened for editing.

**Approved stack for this phase's declared work** (deterministic, from the stack spec):

- pages (persistence) — serves `unified_stylesheet`
- stylesheet (persistence) — serves `unified_stylesheet`
- fonts (persistence): two weights of JetBrains Mono, .woff2 only, for monospace/code/nav/version text; the reading face is a system font stack with no files — serves `unified_stylesheet`
- images (persistence) — serves `unified_stylesheet`

## Instructions

1. Read rework/baseline/inventory.md and work only through the thirteen styled page paths it lists. Do not open, edit, or reformat any of the ten redirect stubs, any file under examples/, or any existing file under rework/.
2. Reference .spec4/v1/design/mock.html for the intended visual result as you apply the skeleton. It is a look reference only: its front page rewrote the site's headings, its screenshot is hand-drawn HTML with invented figures, and its `<script>` and `main { display: none }` exist solely to hold three pages in one file. None of that is built, and no character of the mock's copy enters any page.
3. For each of the thirteen pages, establish the identical skeleton: `<head>` → `<nav>` → `<main>`, with no footer. Do not add a `<footer>` element to any page — the nav carries the version, and every fact the mock's footer line held is already present on the front page's trust strip.
4. In each page's `<head>`, ensure exactly these elements are present and correct: charset utf-8, `<meta name="viewport" content="width=device-width, initial-scale=1">`, the page title, the existing description and Open Graph tags preserved as they are, the favicon link, and a single `<link rel="stylesheet" href="/styles.css">`. Preserve the existing canonical and social metadata values verbatim — do not rewrite titles, descriptions, or OG values.
5. Remove the Google Fonts `<link>` elements from every one of the thirteen pages — including any `<link rel="preconnect">` to fonts.googleapis.com or fonts.gstatic.com and any `@import` of a Google Fonts URL. After this phase no page requests a byte from any host other than spec4.ai; the JetBrains Mono weights are served from fonts/ by the Phase 2 @font-face rules.
6. Delete any remaining `<style>` block and any `style="..."` attribute from the thirteen pages, so the shared stylesheet is the single source of presentation for the whole site.
7. Replace each page's existing nav with the canonical nav markup contract recorded as a comment at the top of the nav section of styles.css, copied identically onto every page — same elements, same classes, same order, same three links.
8. Set the current-section mark per the contract: `aria-current="page"` on the Docs link for the docs index and all ten docs pages, `aria-current="page"` on the Examples link for bws4/index.html, and no aria-current at all on index.html. Do not add a Home link to index.html or to any other page.
9. Wrap every `<table>` on every page in a `<div class="table-wrap">` per the components markup contract. Add the wrapper only — do not reorder columns, merge cells, change header text, or alter any cell content.
10. Confirm every code block on every page is a `<pre><code>` pair, and strip any leftover syntax-highlighting spans, language classes, or line-number markup from inside them. Removing a highlighting span must not change the characters of the code text itself.
11. Confirm every figure on every page is a `<figure>` containing an `<img>` with a meaningful `alt` followed by a `<figcaption>`, per the components markup contract. If an existing image already carries caption text in a sibling paragraph, move that exact text into the figcaption without rewording it.
12. Remove every class, id, and wrapper element left over from the previous stylesheet that the new stylesheet does not use — hero, card, grid, and container classes in particular. Remove the wrapper element only where doing so changes no text; where a wrapper carries text, strip its class and leave the element.
13. Verify the rendered text of each page against its authoritative copy file under rework/ — the copy files are the text source, and this round changes styles.css and the minimum markup the stylesheet needs, nothing else. If a page's text and its copy file disagree, do not resolve it here: record the discrepancy in rework/baseline/inventory.md under a 'copy drift found' heading and leave the page's text exactly as it is.
14. After editing each page, re-extract its text with rework/baseline/extract_text.py and diff against its file in rework/baseline/text/. The diff must be empty. If it is not, your markup edit changed the copy — revert that edit and redo it structurally.
15. Confirm no page loads any resource except its own HTML, /styles.css, the two self-hosted fonts, and its own images. Add no script tag, no analytics snippet, and no third-party embed to any page.

## Risk Assessment

**Potential bottlenecks:**

Thirteen files edited by hand is where drift enters: a nav copied with a typo onto page seven, a stray class kept on page eleven 'because it looked needed', an aria-current left on the front page. The sharper risk is copy damage — unwrapping a leftover container div or stripping a highlighting span is exactly the kind of edit that silently swallows a text node, and a missing word is invisible to visual inspection across thirteen pages. A third risk is an agent treating the mock as a content source and rewriting a heading to match it.

**Mitigation strategy:**

The nav and the three components are applied from markup contracts that live as comments inside styles.css itself, so all thirteen pages copy one written structure rather than each being re-derived. Copy damage is caught mechanically rather than visually: every page is re-extracted with the Phase 1 script and diffed against its baseline immediately after editing, and a non-empty diff means the edit is reverted and redone — the baseline exists precisely because this phase runs in a fresh session with no memory of the original text. The mock's status as a look-only reference is stated in the instructions, and the byte-identity diff would catch any copy borrowed from it. Copy drift discovered against the rework/ files is recorded rather than fixed, keeping this round's change confined to presentation.

## Verification

Run `grep -rniE 'fonts\.googleapis|fonts\.gstatic|@import' --include=index.html .` and expect no matches: no `<link>` or `@import` to any host other than spec4.ai exists on any of the thirteen pages. Run `grep -rn '<script' --include=index.html .` and expect no matches, satisfying nfr_every_page_loads_and_renders_correctly_without_requiring_any_script_to_run. Run `grep -rn '<footer' --include=index.html .` and expect no matches on the thirteen styled pages. Run `grep -rc 'styles.css' --include=index.html .` and confirm each of the thirteen pages links it exactly once and each of the ten stubs links it zero times. Run `grep -rn 'aria-current' --include=index.html .` and confirm exactly twelve matches — the docs index, the ten docs pages, and bws4 — with none on index.html. Confirm every `<table>` in the thirteen pages is preceded by a `<div class="table-wrap">`. Re-extract all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, proving the rendered copy is byte-identical before and after. Load each page from the local server with the Network panel open and confirm the only requests are the page, /styles.css, the two .woff2 files, and that page's own images, satisfying nfr_pages_load_quickly_even_on_slow_connections__given_they_contain_no_scripts__media_playback__or_heavy_assets and nfr_the_site_collects_no_analytics_or_tracking_information_about_readers.

**Non-functional acceptance** (deterministic, from the stack spec):

- `nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout`: Pages remain fully readable and navigable on narrow viewports without horizontal breakage of the overall layout — delivered by stylesheet
- `nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes`: Text and code remain readable at sufficient contrast in both light and dark reading schemes — delivered by stylesheet
- `nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages`: The shared visual presentation can be updated once and take effect consistently across all pages — delivered by stylesheet


## References

- [WHATWG HTML Living Standard](https://html.spec.whatwg.org/multipage/)
- [WHATWG HTML Living Standard (meta http-equiv=refresh, used by the redirect stubs)](https://html.spec.whatwg.org/multipage/semantics.html#attr-meta-http-equiv-refresh)
- [Open Graph protocol](https://ogp.me)
- [ARIA aria-current attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-current)
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
