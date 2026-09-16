---
{
  "phase_number": 5,
  "total_phases": 7,
  "phase_title": "Components — Table Wrapper, Code Panel, Figure",
  "phase_summary": "Build the three content components that carry this round's entire layout risk: tables that scroll inside a bounded wrapper, code blocks as plain scrollable panels with no syntax coloring and no line numbers, and figures at full column width with a visible caption — and record the markup contract Phase 6 applies to the pages.",
  "features": [
    {
      "id": "unified_stylesheet",
      "role": "extended",
      "scope_note": "Adds the table wrapper, code panel, and figure component styles plus their markup contracts; the wrappers and classes are applied to the thirteen pages' HTML in Phase 6."
    }
  ],
  "capabilities": [],
  "tech_stack_spec": {
    "dependencies": [],
    "configurations": "Edits styles.css only, in the `components` section between the nav section and the page-specific overrides section. All colors come from Phase 2 tokens; code and table cells use --font-mono where appropriate. This section contains the only overflow declarations in the stylesheet, and every one of them is scoped to a bounded container — never to html, body, or main."
  },
  "instructions": [
    "Add a `/* components (table wrapper, code panel, figure) */` section header comment to styles.css after the nav section, and confine every rule in this phase to it.",
    "Reference .spec4/v1/design/mock.html for the intended look of tables, code panels, and figures. Read the mock for visual treatment only — its screenshot is drawn as HTML with invented figure content and is not a source of images or copy.",
    "Write the components markup contract as a comment block at the top of the components section, so Phase 6 has one authoritative structure: every `<table>` is wrapped in a `<div class=\"table-wrap\">`; every code block is a `<pre><code>` pair; every figure is a `<figure>` containing an `<img>` followed by a `<figcaption>`. State that Phase 6 adds the table wrapper as the minimum markup the stylesheet needs and changes no table content.",
    "Style `.table-wrap` with `overflow-x: auto` and `-webkit-overflow-scrolling: touch` omitted (no vendor prefixes are used in this project), so a wide table scrolls inside its own bounded area rather than forcing the page to scroll. Give the wrapper a bottom margin matching the paragraph rhythm.",
    "Add `max-width: 100%` to `.table-wrap` so the wrapper itself can never exceed the reading column, and set the inner `table` to `min-width` sized so columns stay legible while the wrapper handles the overflow — the table is allowed to be wider than the wrapper; that is the mechanism.",
    "Style the table itself with `border-collapse: collapse`, left-aligned cells, padding on th and td, a 1px bottom rule on rows using the --color-rule token, and a header row distinguished by weight rather than by a background fill. Add no zebra striping, no cell backgrounds, no rounded corners, and no borders around the table as a whole.",
    "Style `pre` as a plain scrollable panel: --color-code-tint background, padding, `overflow-x: auto`, `white-space: pre`, and no wrapping. Apply --font-mono and set a line-height comfortable for reading multi-line samples.",
    "Set `pre` to `max-width: 100%` so a long code line scrolls inside the panel and never widens the page, and remove any rounding, border, or shadow from the panel — it is a flat tinted block.",
    "Style `pre code` to inherit the panel's font and size and to carry no background or padding of its own, so the inline-code styling from Phase 3 does not double-apply inside a panel.",
    "Add no syntax coloring and no line numbers, and add no rule that could produce either — no `::before` counter on code lines, no per-token color classes, no language-specific selectors. The code panel's only colors are the panel tint and the base text color.",
    "Style `figure` at full column width with zero horizontal margin, and set its `img` to `max-width: 100%; height: auto; display: block` so images scale down on narrow viewports without overflowing.",
    "Style `figcaption` below the image in the reading typeface at a reduced size using the --color-muted token, with clear space between the image and its caption. The caption must be visibly present, never a hover-revealed tooltip.",
    "Run a final scan of the components section confirming it introduced no icon, card shape, hero, shadow, gradient, animation, or second accent color, and that the only overflow declarations in the whole stylesheet are the ones on `.table-wrap` and `pre`.",
    "To check your work without touching repository markup, create a throwaway file at /tmp/components-check.html linking styles.css and containing: a table of at least eight columns wrapped in `.table-wrap`, a `<pre><code>` block with one line well over 120 characters, and a `<figure>` with an image from the repository and a `<figcaption>`. Do not commit this file and do not place it inside the repository."
  ],
  "risk_assessment": {
    "potential_bottlenecks": "This phase is where the narrow-viewport guarantee is actually won or lost, and the classic failure is subtle: setting `overflow-x: auto` on the wrapper while leaving the table at `width: 100%`, which makes the table shrink instead of scroll and squeezes columns into unreadable slivers — the page looks fine at 380px and the guarantee is quietly broken. The inverse failure is reaching for `overflow-x: hidden` on body to suppress a page-level scrollbar, which is precisely the rule Phase 2 deleted and which would mask every overflow bug from Phase 7's checks.",
    "mitigation_strategy": "The wrapper/table relationship is stated explicitly as the mechanism — the wrapper is bounded and scrolls, the table is permitted to exceed it via min-width — rather than left to the agent to derive. Verification requires a table of at least eight columns and a code line over 120 characters in the scratch file, so both components are exercised past their limits at 380px rather than tested with content that happens to fit. Verification also greps the whole stylesheet to confirm every overflow declaration is scoped to .table-wrap or pre, which mechanically prevents a body-level overflow rule from reappearing."
  },
  "verification": "Open /tmp/components-check.html at 380px: the eight-column table scrolls horizontally inside its own bounded wrapper with columns still legible, the long code line scrolls inside the code panel, the figure image scales down with its caption visible below it, and the document body itself does not scroll horizontally — satisfying nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout. Run `grep -n 'overflow' styles.css` and confirm every match is scoped to .table-wrap or pre, with no match on html, body, or main. Run `grep -niE 'shadow|gradient|animation|transition|border-radius|counter-increment' styles.css` and expect no matches. Confirm the code panel shows no syntax coloring and no line numbers. Toggle the OS between light and dark appearance and confirm table rules, code panel tint, and caption text all remain legible, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.",
  "references": [
    {
      "standard": "CSS overflow property",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/overflow"
    },
    {
      "standard": "HTML figure and figcaption elements",
      "url": "https://html.spec.whatwg.org/multipage/grouping-content.html#the-figure-element"
    },
    {
      "standard": "HTML table element",
      "url": "https://html.spec.whatwg.org/multipage/tables.html#the-table-element"
    },
    {
      "standard": "WCAG 2.1 SC 1.4.3 Contrast (Minimum)",
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum"
    }
  ]
}
---

# Phase 5 of 7: Components — Table Wrapper, Code Panel, Figure

Build the three content components that carry this round's entire layout risk: tables that scroll inside a bounded wrapper, code blocks as plain scrollable panels with no syntax coloring and no line numbers, and figures at full column width with a visible caption — and record the markup contract Phase 6 applies to the pages.

## Feature Specifications

These specifications are authoritative for this phase. Implement to them; the instructions below tell you how and in what order.

### Unified_Stylesheet — product feature — extended in this phase

*Scope for this phase: Adds the table wrapper, code panel, and figure component styles plus their markup contracts; the wrappers and classes are applied to the thirteen pages' HTML in Phase 6.*

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

**Configurations:** Edits styles.css only, in the `components` section between the nav section and the page-specific overrides section. All colors come from Phase 2 tokens; code and table cells use --font-mono where appropriate. This section contains the only overflow declarations in the stylesheet, and every one of them is scoped to a bounded container — never to html, body, or main.

**Approved stack for this phase's declared work** (deterministic, from the stack spec):

- pages (persistence) — serves `unified_stylesheet`
- stylesheet (persistence) — serves `unified_stylesheet`
- fonts (persistence): two weights of JetBrains Mono, .woff2 only, for monospace/code/nav/version text; the reading face is a system font stack with no files — serves `unified_stylesheet`
- images (persistence) — serves `unified_stylesheet`

## Instructions

1. Add a `/* components (table wrapper, code panel, figure) */` section header comment to styles.css after the nav section, and confine every rule in this phase to it.
2. Reference .spec4/v1/design/mock.html for the intended look of tables, code panels, and figures. Read the mock for visual treatment only — its screenshot is drawn as HTML with invented figure content and is not a source of images or copy.
3. Write the components markup contract as a comment block at the top of the components section, so Phase 6 has one authoritative structure: every `<table>` is wrapped in a `<div class="table-wrap">`; every code block is a `<pre><code>` pair; every figure is a `<figure>` containing an `<img>` followed by a `<figcaption>`. State that Phase 6 adds the table wrapper as the minimum markup the stylesheet needs and changes no table content.
4. Style `.table-wrap` with `overflow-x: auto` and `-webkit-overflow-scrolling: touch` omitted (no vendor prefixes are used in this project), so a wide table scrolls inside its own bounded area rather than forcing the page to scroll. Give the wrapper a bottom margin matching the paragraph rhythm.
5. Add `max-width: 100%` to `.table-wrap` so the wrapper itself can never exceed the reading column, and set the inner `table` to `min-width` sized so columns stay legible while the wrapper handles the overflow — the table is allowed to be wider than the wrapper; that is the mechanism.
6. Style the table itself with `border-collapse: collapse`, left-aligned cells, padding on th and td, a 1px bottom rule on rows using the --color-rule token, and a header row distinguished by weight rather than by a background fill. Add no zebra striping, no cell backgrounds, no rounded corners, and no borders around the table as a whole.
7. Style `pre` as a plain scrollable panel: --color-code-tint background, padding, `overflow-x: auto`, `white-space: pre`, and no wrapping. Apply --font-mono and set a line-height comfortable for reading multi-line samples.
8. Set `pre` to `max-width: 100%` so a long code line scrolls inside the panel and never widens the page, and remove any rounding, border, or shadow from the panel — it is a flat tinted block.
9. Style `pre code` to inherit the panel's font and size and to carry no background or padding of its own, so the inline-code styling from Phase 3 does not double-apply inside a panel.
10. Add no syntax coloring and no line numbers, and add no rule that could produce either — no `::before` counter on code lines, no per-token color classes, no language-specific selectors. The code panel's only colors are the panel tint and the base text color.
11. Style `figure` at full column width with zero horizontal margin, and set its `img` to `max-width: 100%; height: auto; display: block` so images scale down on narrow viewports without overflowing.
12. Style `figcaption` below the image in the reading typeface at a reduced size using the --color-muted token, with clear space between the image and its caption. The caption must be visibly present, never a hover-revealed tooltip.
13. Run a final scan of the components section confirming it introduced no icon, card shape, hero, shadow, gradient, animation, or second accent color, and that the only overflow declarations in the whole stylesheet are the ones on `.table-wrap` and `pre`.
14. To check your work without touching repository markup, create a throwaway file at /tmp/components-check.html linking styles.css and containing: a table of at least eight columns wrapped in `.table-wrap`, a `<pre><code>` block with one line well over 120 characters, and a `<figure>` with an image from the repository and a `<figcaption>`. Do not commit this file and do not place it inside the repository.

## Risk Assessment

**Potential bottlenecks:**

This phase is where the narrow-viewport guarantee is actually won or lost, and the classic failure is subtle: setting `overflow-x: auto` on the wrapper while leaving the table at `width: 100%`, which makes the table shrink instead of scroll and squeezes columns into unreadable slivers — the page looks fine at 380px and the guarantee is quietly broken. The inverse failure is reaching for `overflow-x: hidden` on body to suppress a page-level scrollbar, which is precisely the rule Phase 2 deleted and which would mask every overflow bug from Phase 7's checks.

**Mitigation strategy:**

The wrapper/table relationship is stated explicitly as the mechanism — the wrapper is bounded and scrolls, the table is permitted to exceed it via min-width — rather than left to the agent to derive. Verification requires a table of at least eight columns and a code line over 120 characters in the scratch file, so both components are exercised past their limits at 380px rather than tested with content that happens to fit. Verification also greps the whole stylesheet to confirm every overflow declaration is scoped to .table-wrap or pre, which mechanically prevents a body-level overflow rule from reappearing.

## Verification

Open /tmp/components-check.html at 380px: the eight-column table scrolls horizontally inside its own bounded wrapper with columns still legible, the long code line scrolls inside the code panel, the figure image scales down with its caption visible below it, and the document body itself does not scroll horizontally — satisfying nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout. Run `grep -n 'overflow' styles.css` and confirm every match is scoped to .table-wrap or pre, with no match on html, body, or main. Run `grep -niE 'shadow|gradient|animation|transition|border-radius|counter-increment' styles.css` and expect no matches. Confirm the code panel shows no syntax coloring and no line numbers. Toggle the OS between light and dark appearance and confirm table rules, code panel tint, and caption text all remain legible, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.

**Non-functional acceptance** (deterministic, from the stack spec):

- `nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout`: Pages remain fully readable and navigable on narrow viewports without horizontal breakage of the overall layout — delivered by stylesheet
- `nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes`: Text and code remain readable at sufficient contrast in both light and dark reading schemes — delivered by stylesheet
- `nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages`: The shared visual presentation can be updated once and take effect consistently across all pages — delivered by stylesheet


## References

- [CSS overflow property](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow)
- [HTML figure and figcaption elements](https://html.spec.whatwg.org/multipage/grouping-content.html#the-figure-element)
- [HTML table element](https://html.spec.whatwg.org/multipage/tables.html#the-table-element)
- [WCAG 2.1 SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)
