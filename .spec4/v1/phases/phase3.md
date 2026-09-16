---
{
  "phase_number": 3,
  "total_phases": 7,
  "phase_title": "Base Element Typography — The Reading Layout",
  "phase_summary": "Build the base-element layer of styles.css on top of Phase 2's tokens: the reading column at proper measure and line-height, headings, paragraphs, links, lists, inline code, and rules — the reading typeface for prose, the monospace face reserved for code, filenames, and version text.",
  "features": [
    {
      "id": "unified_stylesheet",
      "role": "extended",
      "scope_note": "Adds the base-element typography and reading-column layout; the nav lands in Phase 4, the table/code/figure components in Phase 5, and application to the thirteen pages in Phase 6."
    }
  ],
  "capabilities": [],
  "tech_stack_spec": {
    "dependencies": [],
    "configurations": "Edits styles.css only, in the `base elements` section that follows the tokens section and precedes the nav section. All colors and fonts are referenced through the Phase 2 :root custom properties via var(); no literal color or font-family is written in this phase."
  },
  "instructions": [
    "Add a `/* base elements */` section header comment to styles.css immediately after Phase 2's dark-scheme block, and write every rule in this phase inside that section — never above the tokens, never below the point where the nav section will begin.",
    "Reference .spec4/v1/design/mock.html for the intended type scale, spacing rhythm, and heading weights. Read it for look only: take no copy, no headings, no script, and none of its page-switching CSS from it.",
    "Set `box-sizing: border-box` on all elements via the universal selector and the ::before/::after pseudo-elements, then set html and body to use --color-bg for background and --color-text for color, and the --font-prose token for the body font.",
    "Style the reading column: constrain `main` to the max-measure token, center it horizontally with auto side margins, and give it horizontal padding so text never touches the viewport edge at 380px. Do not set overflow on body or main — bounded scrolling belongs only to the Phase 5 components.",
    "Set the body line-height and base font-size from the Phase 2 tokens, and set paragraph margins so vertical rhythm is consistent; use margin-block on paragraphs rather than a mix of top and bottom margins that would collapse unpredictably.",
    "Style h1 through h4 with a clear descending scale in the reading typeface, with more space above a heading than below it so headings group with the text they introduce. Give each heading a `scroll-margin-top` so in-page anchor links do not land with the heading flush against the viewport top.",
    "Style links using the --color-text token with an underline; do not introduce a link color. The wordmark's two-color treatment must remain the only place blue appears on the site, as the attached specification's success criteria require — so no link, heading, or accent in this phase may use the blue or green wordmark tokens.",
    "Give links a visible `:focus-visible` outline using an existing token so keyboard navigation is usable without introducing a new color.",
    "Style ul and ol with restrained left padding and list-item spacing that matches the paragraph rhythm; do not add custom bullet glyphs, icons, or markers.",
    "Style inline `code` (code not inside a pre) with the --font-mono token, a slightly reduced font-size so it sits on the prose baseline without inflating line-height, and the --color-code-tint background token with small horizontal padding. Do not style `pre` in this phase — the code panel is a Phase 5 component.",
    "Style `hr` as a single 1px rule using the --color-rule token with generous vertical margin, with no border-style flourishes.",
    "Style `strong` and `em` with weight and italics only. Add no text-shadow, no letter-spacing tricks, and no decorative first-letter or first-line rules.",
    "Confirm this phase introduced no shadow, gradient, animation, transition, transform, icon, card, or hero rule — the exclusion list is a standing constraint checked on every change to the shared presentation, per the attached specification's failure modes.",
    "To check your work without touching repository markup, create a throwaway file at /tmp/type-check.html that links ../styles.css (or an absolute path to it) and contains a heading hierarchy, two paragraphs of filler prose, a link, a list, and an inline code span. Do not commit this file and do not place it anywhere inside the repository."
  ],
  "risk_assessment": {
    "potential_bottlenecks": "The most likely error is scope creep into components: styling `pre`, `table`, or `figure` here, which then collides with Phase 5 and produces two competing definitions for the same element in one file. A second is re-introducing a literal color — an agent that writes `color: #333` for muted text breaks the single-source-of-update guarantee and silently defeats the dark scheme, because a literal will not swap inside the prefers-color-scheme block.",
    "mitigation_strategy": "Every rule is confined to the explicitly named `base elements` section between the two section-header comments, and the phase instructions state that pre, table, and figure are out of scope. Verification greps for hex and rgb() literals outside the :root and dark-scheme blocks, so a hard-coded color fails the phase mechanically rather than surviving to be discovered in dark mode later. Dark-mode correctness is checked in this phase rather than deferred, by toggling the OS setting against the scratch file."
  },
  "verification": "Open /tmp/type-check.html in a browser at 380px and at 1280px: body text sits in a centered column at comfortable measure, never touches the viewport edge, and the document body does not scroll horizontally at either width. Toggle the OS between light and dark appearance and confirm all base text and inline code remain readable with no rule needing a second definition, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Run `grep -nE '#[0-9a-fA-F]{3,8}|rgb\\(|hsl\\(' styles.css` and confirm every match falls inside the :root block or the prefers-color-scheme block, satisfying nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages. Run `grep -niE 'shadow|gradient|animation|transition|transform|@keyframes' styles.css` and expect no matches. Confirm the wordmark blue and green tokens are referenced nowhere in the base-elements section. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.",
  "references": [
    {
      "standard": "CSS custom properties (--*): CSS variables",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/--*"
    },
    {
      "standard": "prefers-color-scheme (CSS media feature)",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme"
    },
    {
      "standard": "WCAG 2.1 SC 1.4.3 Contrast (Minimum)",
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum"
    }
  ]
}
---

# Phase 3 of 7: Base Element Typography — The Reading Layout

Build the base-element layer of styles.css on top of Phase 2's tokens: the reading column at proper measure and line-height, headings, paragraphs, links, lists, inline code, and rules — the reading typeface for prose, the monospace face reserved for code, filenames, and version text.

## Feature Specifications

These specifications are authoritative for this phase. Implement to them; the instructions below tell you how and in what order.

### Unified_Stylesheet — product feature — extended in this phase

*Scope for this phase: Adds the base-element typography and reading-column layout; the nav lands in Phase 4, the table/code/figure components in Phase 5, and application to the thirteen pages in Phase 6.*

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

**Configurations:** Edits styles.css only, in the `base elements` section that follows the tokens section and precedes the nav section. All colors and fonts are referenced through the Phase 2 :root custom properties via var(); no literal color or font-family is written in this phase.

**Approved stack for this phase's declared work** (deterministic, from the stack spec):

- pages (persistence) — serves `unified_stylesheet`
- stylesheet (persistence) — serves `unified_stylesheet`
- fonts (persistence): two weights of JetBrains Mono, .woff2 only, for monospace/code/nav/version text; the reading face is a system font stack with no files — serves `unified_stylesheet`
- images (persistence) — serves `unified_stylesheet`

## Instructions

1. Add a `/* base elements */` section header comment to styles.css immediately after Phase 2's dark-scheme block, and write every rule in this phase inside that section — never above the tokens, never below the point where the nav section will begin.
2. Reference .spec4/v1/design/mock.html for the intended type scale, spacing rhythm, and heading weights. Read it for look only: take no copy, no headings, no script, and none of its page-switching CSS from it.
3. Set `box-sizing: border-box` on all elements via the universal selector and the ::before/::after pseudo-elements, then set html and body to use --color-bg for background and --color-text for color, and the --font-prose token for the body font.
4. Style the reading column: constrain `main` to the max-measure token, center it horizontally with auto side margins, and give it horizontal padding so text never touches the viewport edge at 380px. Do not set overflow on body or main — bounded scrolling belongs only to the Phase 5 components.
5. Set the body line-height and base font-size from the Phase 2 tokens, and set paragraph margins so vertical rhythm is consistent; use margin-block on paragraphs rather than a mix of top and bottom margins that would collapse unpredictably.
6. Style h1 through h4 with a clear descending scale in the reading typeface, with more space above a heading than below it so headings group with the text they introduce. Give each heading a `scroll-margin-top` so in-page anchor links do not land with the heading flush against the viewport top.
7. Style links using the --color-text token with an underline; do not introduce a link color. The wordmark's two-color treatment must remain the only place blue appears on the site, as the attached specification's success criteria require — so no link, heading, or accent in this phase may use the blue or green wordmark tokens.
8. Give links a visible `:focus-visible` outline using an existing token so keyboard navigation is usable without introducing a new color.
9. Style ul and ol with restrained left padding and list-item spacing that matches the paragraph rhythm; do not add custom bullet glyphs, icons, or markers.
10. Style inline `code` (code not inside a pre) with the --font-mono token, a slightly reduced font-size so it sits on the prose baseline without inflating line-height, and the --color-code-tint background token with small horizontal padding. Do not style `pre` in this phase — the code panel is a Phase 5 component.
11. Style `hr` as a single 1px rule using the --color-rule token with generous vertical margin, with no border-style flourishes.
12. Style `strong` and `em` with weight and italics only. Add no text-shadow, no letter-spacing tricks, and no decorative first-letter or first-line rules.
13. Confirm this phase introduced no shadow, gradient, animation, transition, transform, icon, card, or hero rule — the exclusion list is a standing constraint checked on every change to the shared presentation, per the attached specification's failure modes.
14. To check your work without touching repository markup, create a throwaway file at /tmp/type-check.html that links ../styles.css (or an absolute path to it) and contains a heading hierarchy, two paragraphs of filler prose, a link, a list, and an inline code span. Do not commit this file and do not place it anywhere inside the repository.

## Risk Assessment

**Potential bottlenecks:**

The most likely error is scope creep into components: styling `pre`, `table`, or `figure` here, which then collides with Phase 5 and produces two competing definitions for the same element in one file. A second is re-introducing a literal color — an agent that writes `color: #333` for muted text breaks the single-source-of-update guarantee and silently defeats the dark scheme, because a literal will not swap inside the prefers-color-scheme block.

**Mitigation strategy:**

Every rule is confined to the explicitly named `base elements` section between the two section-header comments, and the phase instructions state that pre, table, and figure are out of scope. Verification greps for hex and rgb() literals outside the :root and dark-scheme blocks, so a hard-coded color fails the phase mechanically rather than surviving to be discovered in dark mode later. Dark-mode correctness is checked in this phase rather than deferred, by toggling the OS setting against the scratch file.

## Verification

Open /tmp/type-check.html in a browser at 380px and at 1280px: body text sits in a centered column at comfortable measure, never touches the viewport edge, and the document body does not scroll horizontally at either width. Toggle the OS between light and dark appearance and confirm all base text and inline code remain readable with no rule needing a second definition, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Run `grep -nE '#[0-9a-fA-F]{3,8}|rgb\(|hsl\(' styles.css` and confirm every match falls inside the :root block or the prefers-color-scheme block, satisfying nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages. Run `grep -niE 'shadow|gradient|animation|transition|transform|@keyframes' styles.css` and expect no matches. Confirm the wordmark blue and green tokens are referenced nowhere in the base-elements section. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.

**Non-functional acceptance** (deterministic, from the stack spec):

- `nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout`: Pages remain fully readable and navigable on narrow viewports without horizontal breakage of the overall layout — delivered by stylesheet
- `nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes`: Text and code remain readable at sufficient contrast in both light and dark reading schemes — delivered by stylesheet
- `nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages`: The shared visual presentation can be updated once and take effect consistently across all pages — delivered by stylesheet


## References

- [CSS custom properties (--*): CSS variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/--*)
- [prefers-color-scheme (CSS media feature)](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme)
- [WCAG 2.1 SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)
