---
{
  "phase_number": 2,
  "total_phases": 7,
  "phase_title": "Replace styles.css — Design Tokens, Self-Hosted Fonts & the Dark Scheme",
  "phase_summary": "Delete the previous stylesheet outright and write a new styles.css containing only three things: the :root design-token block, the @font-face declarations for the two self-hosted JetBrains Mono weights, and the prefers-color-scheme dark block. No rule from the old file survives unless a later phase re-decides it deliberately; the pages render essentially unstyled until Phase 6, which is correct because nothing deploys mid-round.",
  "features": [
    {
      "id": "unified_stylesheet",
      "role": "introduced",
      "scope_note": "Establishes the color and font token layer, the self-hosted webfonts, and the system-driven light/dark scheme; base typography, nav, components, and page application all land in Phases 3-6."
    }
  ],
  "capabilities": [],
  "tech_stack_spec": {
    "dependencies": [],
    "configurations": "No env vars, no build step, no preprocessor, no vendor prefixes. styles.css lives at the repository root. Font files are the two JetBrains Mono .woff2 weights under fonts/, referenced by root-relative url() paths. CSS custom properties are kebab-case (e.g. --color-bg, --font-mono) and declared on :root; quoted values use double quotes; indentation is 2 spaces."
  },
  "instructions": [
    "Delete the entire contents of styles.css and write the new file from scratch. Do not preserve, comment out, or migrate any rule from the previous stylesheet. In particular the old `body { overflow-x: hidden }` rule, the old nav rules, and all hero, card, and grid rule sets are removed and are not re-added in this or any later phase — Phase 5 contains the site's only overflow handling, and it is scoped to bounded containers, never to the body.",
    "Open .spec4/v1/design/mock.html and read it strictly as a look reference for colors and typography. Do not copy its copy, its headings, its `<script>`, its `main { display: none }` rule, or its hand-drawn HTML screenshot — those exist only to hold three pages in one file and none of them get built.",
    "Write a section-header comment at the top of styles.css declaring the mandated file order and stating that the order must be preserved by every later edit: tokens → base elements → nav → components (table wrapper, code panel, figure) → page-specific overrides.",
    "Under a `/* tokens */` section header, declare a :root block holding every color and every font as a custom property. Sample the exact color values from the mock rather than inventing them: background, primary text, muted text, rule/border, code panel tint, the wordmark's Spec blue, and the wordmark's 4 green. Declare no other color anywhere in the file — every later phase references these properties via var() and never writes a literal color.",
    "Declare exactly two font tokens: --font-mono set to the self-hosted JetBrains Mono family with a generic monospace fallback, and --font-prose set to a system font stack (no font files are shipped for the reading typeface and no webfont is downloaded for it).",
    "Declare the measure and rhythm tokens the later phases share — reading-column max width, base line-height, and the base font size — as custom properties on :root, so the reading layout is adjusted in one place.",
    "Under the same tokens section, write two @font-face rules for the two JetBrains Mono weights, each pointing at its .woff2 file under fonts/ with `format(\"woff2\")`, each with an explicit font-weight matching the file's weight, font-style normal, and `font-display: swap`. Reference only the .woff2 files that exist in fonts/ — do not add formats, weights, or files that are not in the repository.",
    "Confirm that no @font-face rule and no token references any third-party host. All font bytes are served from this repository; the site makes no runtime request to Google Fonts or any other origin.",
    "Add a `@media (prefers-color-scheme: dark)` block immediately after the token block that redefines the color custom properties — and only the color properties — with their dark-scheme counterparts sampled from the mock. Do not duplicate any structural rule inside the media query; dark mode is a token swap and nothing else.",
    "Do not add any element, class, attribute, or rule that could serve as a color-scheme toggle. The scheme is driven purely by the reader's system-level preference, as the attached specification's success criteria and failure modes require.",
    "Check the contrast ratio of primary text on background, and of muted text on background, in both the light tokens and the dark tokens, against WCAG 2.1 SC 1.4.3 (4.5:1 for body text). If a sampled pair falls short, darken or lighten the muted or text token until it passes and record the adjusted value in a comment beside the token.",
    "Add `color-scheme: light dark` to the :root block so form controls, scrollbars, and the canvas follow the active scheme natively.",
    "Do not add any base element, nav, or component rules in this phase. The file ends after the dark-scheme block."
  ],
  "risk_assessment": {
    "potential_bottlenecks": "The highest-probability failure is an incomplete replacement: the agent keeps parts of the old stylesheet 'to avoid breaking things', leaving the old nav, hero, card, or grid rules to collide with Phases 4 and 5 and producing two stylesheets inside one file. The old `body { overflow-x: hidden }` rule is especially dangerous because it silently masks the exact narrow-viewport overflow that Phase 7 must detect. A second bottleneck is @font-face path and format errors, which fail silently — the browser falls back to a generic monospace and nothing visibly errors.",
    "mitigation_strategy": "The instruction is to delete the file's contents and write from scratch, and the verification asserts by name that the old overflow rule and the hero/card/grid selectors are absent from the new file, so the replacement is checked rather than assumed. For the fonts, verification requires opening the browser's Network panel and confirming both .woff2 files return HTTP 200 from the local server, which converts a silent fallback into an observable failure. Colors are sampled from the finalized mock rather than invented, and every contrast pair is checked numerically against SC 1.4.3 before the phase closes."
  },
  "verification": "No rule from the previous styles.css survives except by having been re-decided in a later phase — confirm with `grep -n 'overflow-x' styles.css` (expect no body-level match), and `grep -niE 'hero|card|grid|shadow|gradient|animation|transition' styles.css` (expect no matches). Confirm `grep -c 'font-face' styles.css` returns 2 and `grep -n 'fonts.googleapis\\|fonts.gstatic\\|http' styles.css` returns nothing. Load any page from the local server and confirm in the browser Network panel that both fonts/*.woff2 files return HTTP 200 and no request goes to a third-party host. Toggle the OS between light and dark appearance and confirm the computed value of --color-bg on :root changes with no control present anywhere on the page. Measure primary-text-on-background and muted-text-on-background contrast in both schemes and confirm both meet 4.5:1, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Confirm every color and font in the file is declared once on :root and referenced via var(), satisfying nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages. Confirm no request to any analytics or third-party origin is made, satisfying nfr_the_site_collects_no_analytics_or_tracking_information_about_readers. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.",
  "references": [
    {
      "standard": "prefers-color-scheme (CSS media feature)",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme"
    },
    {
      "standard": "CSS custom properties (--*): CSS variables",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/--*"
    },
    {
      "standard": "@font-face (CSS at-rule)",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face"
    },
    {
      "standard": "WOFF2 File Format",
      "url": "https://www.w3.org/TR/WOFF2/"
    },
    {
      "standard": "WCAG 2.1 SC 1.4.3 Contrast (Minimum)",
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum"
    },
    {
      "standard": "JetBrains Mono (self-hosted typeface)",
      "url": "https://www.jetbrains.com/lp/mono/"
    }
  ]
}
---

# Phase 2 of 7: Replace styles.css — Design Tokens, Self-Hosted Fonts & the Dark Scheme

Delete the previous stylesheet outright and write a new styles.css containing only three things: the :root design-token block, the @font-face declarations for the two self-hosted JetBrains Mono weights, and the prefers-color-scheme dark block. No rule from the old file survives unless a later phase re-decides it deliberately; the pages render essentially unstyled until Phase 6, which is correct because nothing deploys mid-round.

## Feature Specifications

These specifications are authoritative for this phase. Implement to them; the instructions below tell you how and in what order.

### Unified_Stylesheet — product feature — introduced in this phase

*Scope for this phase: Establishes the color and font token layer, the self-hosted webfonts, and the system-driven light/dark scheme; base typography, nav, components, and page application all land in Phases 3-6.*

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

**Configurations:** No env vars, no build step, no preprocessor, no vendor prefixes. styles.css lives at the repository root. Font files are the two JetBrains Mono .woff2 weights under fonts/, referenced by root-relative url() paths. CSS custom properties are kebab-case (e.g. --color-bg, --font-mono) and declared on :root; quoted values use double quotes; indentation is 2 spaces.

**Approved stack for this phase's declared work** (deterministic, from the stack spec):

- pages (persistence) — serves `unified_stylesheet`
- stylesheet (persistence) — serves `unified_stylesheet`
- fonts (persistence): two weights of JetBrains Mono, .woff2 only, for monospace/code/nav/version text; the reading face is a system font stack with no files — serves `unified_stylesheet`
- images (persistence) — serves `unified_stylesheet`

## Instructions

1. Delete the entire contents of styles.css and write the new file from scratch. Do not preserve, comment out, or migrate any rule from the previous stylesheet. In particular the old `body { overflow-x: hidden }` rule, the old nav rules, and all hero, card, and grid rule sets are removed and are not re-added in this or any later phase — Phase 5 contains the site's only overflow handling, and it is scoped to bounded containers, never to the body.
2. Open .spec4/v1/design/mock.html and read it strictly as a look reference for colors and typography. Do not copy its copy, its headings, its `<script>`, its `main { display: none }` rule, or its hand-drawn HTML screenshot — those exist only to hold three pages in one file and none of them get built.
3. Write a section-header comment at the top of styles.css declaring the mandated file order and stating that the order must be preserved by every later edit: tokens → base elements → nav → components (table wrapper, code panel, figure) → page-specific overrides.
4. Under a `/* tokens */` section header, declare a :root block holding every color and every font as a custom property. Sample the exact color values from the mock rather than inventing them: background, primary text, muted text, rule/border, code panel tint, the wordmark's Spec blue, and the wordmark's 4 green. Declare no other color anywhere in the file — every later phase references these properties via var() and never writes a literal color.
5. Declare exactly two font tokens: --font-mono set to the self-hosted JetBrains Mono family with a generic monospace fallback, and --font-prose set to a system font stack (no font files are shipped for the reading typeface and no webfont is downloaded for it).
6. Declare the measure and rhythm tokens the later phases share — reading-column max width, base line-height, and the base font size — as custom properties on :root, so the reading layout is adjusted in one place.
7. Under the same tokens section, write two @font-face rules for the two JetBrains Mono weights, each pointing at its .woff2 file under fonts/ with `format("woff2")`, each with an explicit font-weight matching the file's weight, font-style normal, and `font-display: swap`. Reference only the .woff2 files that exist in fonts/ — do not add formats, weights, or files that are not in the repository.
8. Confirm that no @font-face rule and no token references any third-party host. All font bytes are served from this repository; the site makes no runtime request to Google Fonts or any other origin.
9. Add a `@media (prefers-color-scheme: dark)` block immediately after the token block that redefines the color custom properties — and only the color properties — with their dark-scheme counterparts sampled from the mock. Do not duplicate any structural rule inside the media query; dark mode is a token swap and nothing else.
10. Do not add any element, class, attribute, or rule that could serve as a color-scheme toggle. The scheme is driven purely by the reader's system-level preference, as the attached specification's success criteria and failure modes require.
11. Check the contrast ratio of primary text on background, and of muted text on background, in both the light tokens and the dark tokens, against WCAG 2.1 SC 1.4.3 (4.5:1 for body text). If a sampled pair falls short, darken or lighten the muted or text token until it passes and record the adjusted value in a comment beside the token.
12. Add `color-scheme: light dark` to the :root block so form controls, scrollbars, and the canvas follow the active scheme natively.
13. Do not add any base element, nav, or component rules in this phase. The file ends after the dark-scheme block.

## Risk Assessment

**Potential bottlenecks:**

The highest-probability failure is an incomplete replacement: the agent keeps parts of the old stylesheet 'to avoid breaking things', leaving the old nav, hero, card, or grid rules to collide with Phases 4 and 5 and producing two stylesheets inside one file. The old `body { overflow-x: hidden }` rule is especially dangerous because it silently masks the exact narrow-viewport overflow that Phase 7 must detect. A second bottleneck is @font-face path and format errors, which fail silently — the browser falls back to a generic monospace and nothing visibly errors.

**Mitigation strategy:**

The instruction is to delete the file's contents and write from scratch, and the verification asserts by name that the old overflow rule and the hero/card/grid selectors are absent from the new file, so the replacement is checked rather than assumed. For the fonts, verification requires opening the browser's Network panel and confirming both .woff2 files return HTTP 200 from the local server, which converts a silent fallback into an observable failure. Colors are sampled from the finalized mock rather than invented, and every contrast pair is checked numerically against SC 1.4.3 before the phase closes.

## Verification

No rule from the previous styles.css survives except by having been re-decided in a later phase — confirm with `grep -n 'overflow-x' styles.css` (expect no body-level match), and `grep -niE 'hero|card|grid|shadow|gradient|animation|transition' styles.css` (expect no matches). Confirm `grep -c 'font-face' styles.css` returns 2 and `grep -n 'fonts.googleapis\|fonts.gstatic\|http' styles.css` returns nothing. Load any page from the local server and confirm in the browser Network panel that both fonts/*.woff2 files return HTTP 200 and no request goes to a third-party host. Toggle the OS between light and dark appearance and confirm the computed value of --color-bg on :root changes with no control present anywhere on the page. Measure primary-text-on-background and muted-text-on-background contrast in both schemes and confirm both meet 4.5:1, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Confirm every color and font in the file is declared once on :root and referenced via var(), satisfying nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages. Confirm no request to any analytics or third-party origin is made, satisfying nfr_the_site_collects_no_analytics_or_tracking_information_about_readers. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.

**Non-functional acceptance** (deterministic, from the stack spec):

- `nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout`: Pages remain fully readable and navigable on narrow viewports without horizontal breakage of the overall layout — delivered by stylesheet
- `nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes`: Text and code remain readable at sufficient contrast in both light and dark reading schemes — delivered by stylesheet
- `nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages`: The shared visual presentation can be updated once and take effect consistently across all pages — delivered by stylesheet


## References

- [prefers-color-scheme (CSS media feature)](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme)
- [CSS custom properties (--*): CSS variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/--*)
- [@font-face (CSS at-rule)](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face)
- [WOFF2 File Format](https://www.w3.org/TR/WOFF2/)
- [WCAG 2.1 SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)
- [JetBrains Mono (self-hosted typeface)](https://www.jetbrains.com/lp/mono/)
