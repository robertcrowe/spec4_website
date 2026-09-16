---
{
  "phase_number": 4,
  "total_phases": 7,
  "phase_title": "Site Navigation & Wordmark",
  "phase_summary": "Build the nav layer of styles.css — the wordmark in Spec blue and 4 green as the only blue on the site, the version in monospace, and three text links with the current section marked — and record the exact canonical nav markup contract that Phase 6 will apply to all thirteen pages.",
  "features": [
    {
      "id": "unified_stylesheet",
      "role": "extended",
      "scope_note": "Adds the nav and wordmark presentation plus the canonical nav markup contract; the contract is applied to the thirteen pages' HTML in Phase 6."
    }
  ],
  "capabilities": [],
  "tech_stack_spec": {
    "dependencies": [],
    "configurations": "Edits styles.css only, in the `nav` section between the base-elements section and the components section. Nav colors come from the Phase 2 --wordmark-blue and --accent-green tokens; the version and nav link text use --font-mono. Class and id names are kebab-case."
  },
  "instructions": [
    "Add a `/* nav */` section header comment to styles.css after the base-elements section and before the point where the components section will begin, and confine every rule in this phase to it.",
    "Reference .spec4/v1/design/mock.html for the nav's visual treatment — wordmark weight, version placement, link spacing, and the rule separating nav from content. Take look only: the mock's front-page headings and copy are not the site's copy and are not used.",
    "Define the canonical nav markup contract and write it verbatim as a comment block at the top of the nav section, so Phase 6 has one authoritative structure to copy onto every page. The contract is: a `<nav class=\"site-nav\">` containing a wordmark link to `/` whose text is split into `<span class=\"wordmark-spec\">Spec</span><span class=\"wordmark-four\">4</span>`, a `<span class=\"nav-version\">` holding the version string, and exactly three text links — Docs to `/docs/`, Examples to `/bws4/`, and GitHub to the project's GitHub URL.",
    "State in that same comment block that the nav contains exactly three links and that there is no Home link: the wordmark itself is the path back to `/`. An agent applying this contract must not invent a fourth link.",
    "State in that same comment block how the current section is marked: `aria-current=\"page\"` is placed on the Docs link for the docs index and all ten docs pages, and on the Examples link for /bws4/. The front page at `/` carries no current mark at all — none of the three links corresponds to `/`, so on index.html no nav link receives aria-current. The external GitHub link is never marked current on any page.",
    "Style `.wordmark-spec` with the --wordmark-blue token and `.wordmark-four` with the --accent-green token, both in --font-mono at the wordmark weight. This is the only rule in the entire stylesheet permitted to use the blue token, as the attached specification's success criteria require.",
    "Remove the wordmark link's underline and any hover color change; the wordmark's two-color treatment is its whole presentation.",
    "Style `.nav-version` in --font-mono at a reduced size using the --color-muted token, placed immediately after the wordmark with clear separation.",
    "Lay out the nav so the wordmark and version sit at the start and the three links group at the end, using flexbox with `align-items: center` and a gap. Constrain the nav's inner width to the same reading-column measure token used by main and center it the same way, so the nav and the content share one left edge on every page.",
    "Style the three nav links in --font-mono at a reduced size using --color-muted, with no underline in their resting state and an underline on hover and on :focus-visible. Add no icons, no separators, no dropdowns, and no mobile hamburger.",
    "Style the current-section indicator with the attribute selector `.site-nav a[aria-current=\"page\"]`: raise the link to --color-text and add a visible underline or bottom rule using the --color-rule token. Do not indicate the current section with color alone and do not use the blue or green tokens for it.",
    "Add a 1px bottom rule below the nav using the --color-rule token, separating it from main with consistent spacing above and below.",
    "Make the nav wrap gracefully rather than overflow: at 380px the wordmark, version, and three links must remain visible and reachable without the nav scrolling horizontally and without the body scrolling horizontally. Use flex-wrap and a row gap rather than a media query that hides links.",
    "To check your work without touching repository markup, create a throwaway file at /tmp/nav-check.html containing three copies of the contract markup — one with no aria-current (the front page case), one with aria-current on Docs, one with aria-current on Examples — plus a paragraph of filler prose. Do not commit this file and do not place it inside the repository."
  ],
  "risk_assessment": {
    "potential_bottlenecks": "Two specific hallucinations are likely here. First, inventing a Home link: an agent that sees a nav with a current-section indicator will reason that the front page must also be markable and add a fourth link, which contradicts the design and adds copy that does not exist in the rework/ source. Second, reaching for the wordmark blue to indicate the active section or to color nav links, which breaks the guarantee that the wordmark is the only blue on the site. A third, smaller risk is a narrow-viewport nav that overflows because the three links are held on one line with the wordmark.",
    "mitigation_strategy": "The no-Home-link rule and the front-page-has-no-current-mark rule are both written into the canonical markup contract that ships as a comment in the stylesheet itself, so the constraint travels with the code into Phase 6 rather than living only in this phase file. The active indicator is specified as a weight/rule treatment explicitly forbidden from using the blue or green tokens, and verification greps to confirm the blue token appears in exactly one rule. The /tmp scratch file carries all three nav states side by side, so the front-page case is visually proven to have no marked link before the contract is applied to any real page."
  },
  "verification": "Open /tmp/nav-check.html at 380px and 1280px: the first nav shows no marked link, the second marks Docs, the third marks Examples, and in all three the nav holds exactly three links with no Home link present. Confirm the nav wraps rather than overflows at 380px and that the document body does not scroll horizontally, satisfying nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout. Run `grep -c 'wordmark-blue' styles.css` and confirm the token is referenced in exactly one rule. Run `grep -niE 'svg|icon|hamburger|dropdown' styles.css` and expect no matches. Toggle the OS between light and dark appearance and confirm the wordmark, version, nav links, and the current-section indicator all remain legible, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Confirm the nav section of styles.css contains the canonical markup contract as a comment block. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.",
  "references": [
    {
      "standard": "ARIA aria-current attribute",
      "url": "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-current"
    },
    {
      "standard": "CSS Flexible Box Layout",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout"
    },
    {
      "standard": "WCAG 2.1 SC 1.4.3 Contrast (Minimum)",
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum"
    }
  ]
}
---

# Phase 4 of 7: Site Navigation & Wordmark

Build the nav layer of styles.css — the wordmark in Spec blue and 4 green as the only blue on the site, the version in monospace, and three text links with the current section marked — and record the exact canonical nav markup contract that Phase 6 will apply to all thirteen pages.

## Feature Specifications

These specifications are authoritative for this phase. Implement to them; the instructions below tell you how and in what order.

### Unified_Stylesheet — product feature — extended in this phase

*Scope for this phase: Adds the nav and wordmark presentation plus the canonical nav markup contract; the contract is applied to the thirteen pages' HTML in Phase 6.*

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

**Configurations:** Edits styles.css only, in the `nav` section between the base-elements section and the components section. Nav colors come from the Phase 2 --wordmark-blue and --accent-green tokens; the version and nav link text use --font-mono. Class and id names are kebab-case.

**Approved stack for this phase's declared work** (deterministic, from the stack spec):

- pages (persistence) — serves `unified_stylesheet`
- stylesheet (persistence) — serves `unified_stylesheet`
- fonts (persistence): two weights of JetBrains Mono, .woff2 only, for monospace/code/nav/version text; the reading face is a system font stack with no files — serves `unified_stylesheet`
- images (persistence) — serves `unified_stylesheet`

## Instructions

1. Add a `/* nav */` section header comment to styles.css after the base-elements section and before the point where the components section will begin, and confine every rule in this phase to it.
2. Reference .spec4/v1/design/mock.html for the nav's visual treatment — wordmark weight, version placement, link spacing, and the rule separating nav from content. Take look only: the mock's front-page headings and copy are not the site's copy and are not used.
3. Define the canonical nav markup contract and write it verbatim as a comment block at the top of the nav section, so Phase 6 has one authoritative structure to copy onto every page. The contract is: a `<nav class="site-nav">` containing a wordmark link to `/` whose text is split into `<span class="wordmark-spec">Spec</span><span class="wordmark-four">4</span>`, a `<span class="nav-version">` holding the version string, and exactly three text links — Docs to `/docs/`, Examples to `/bws4/`, and GitHub to the project's GitHub URL.
4. State in that same comment block that the nav contains exactly three links and that there is no Home link: the wordmark itself is the path back to `/`. An agent applying this contract must not invent a fourth link.
5. State in that same comment block how the current section is marked: `aria-current="page"` is placed on the Docs link for the docs index and all ten docs pages, and on the Examples link for /bws4/. The front page at `/` carries no current mark at all — none of the three links corresponds to `/`, so on index.html no nav link receives aria-current. The external GitHub link is never marked current on any page.
6. Style `.wordmark-spec` with the --wordmark-blue token and `.wordmark-four` with the --accent-green token, both in --font-mono at the wordmark weight. This is the only rule in the entire stylesheet permitted to use the blue token, as the attached specification's success criteria require.
7. Remove the wordmark link's underline and any hover color change; the wordmark's two-color treatment is its whole presentation.
8. Style `.nav-version` in --font-mono at a reduced size using the --color-muted token, placed immediately after the wordmark with clear separation.
9. Lay out the nav so the wordmark and version sit at the start and the three links group at the end, using flexbox with `align-items: center` and a gap. Constrain the nav's inner width to the same reading-column measure token used by main and center it the same way, so the nav and the content share one left edge on every page.
10. Style the three nav links in --font-mono at a reduced size using --color-muted, with no underline in their resting state and an underline on hover and on :focus-visible. Add no icons, no separators, no dropdowns, and no mobile hamburger.
11. Style the current-section indicator with the attribute selector `.site-nav a[aria-current="page"]`: raise the link to --color-text and add a visible underline or bottom rule using the --color-rule token. Do not indicate the current section with color alone and do not use the blue or green tokens for it.
12. Add a 1px bottom rule below the nav using the --color-rule token, separating it from main with consistent spacing above and below.
13. Make the nav wrap gracefully rather than overflow: at 380px the wordmark, version, and three links must remain visible and reachable without the nav scrolling horizontally and without the body scrolling horizontally. Use flex-wrap and a row gap rather than a media query that hides links.
14. To check your work without touching repository markup, create a throwaway file at /tmp/nav-check.html containing three copies of the contract markup — one with no aria-current (the front page case), one with aria-current on Docs, one with aria-current on Examples — plus a paragraph of filler prose. Do not commit this file and do not place it inside the repository.

## Risk Assessment

**Potential bottlenecks:**

Two specific hallucinations are likely here. First, inventing a Home link: an agent that sees a nav with a current-section indicator will reason that the front page must also be markable and add a fourth link, which contradicts the design and adds copy that does not exist in the rework/ source. Second, reaching for the wordmark blue to indicate the active section or to color nav links, which breaks the guarantee that the wordmark is the only blue on the site. A third, smaller risk is a narrow-viewport nav that overflows because the three links are held on one line with the wordmark.

**Mitigation strategy:**

The no-Home-link rule and the front-page-has-no-current-mark rule are both written into the canonical markup contract that ships as a comment in the stylesheet itself, so the constraint travels with the code into Phase 6 rather than living only in this phase file. The active indicator is specified as a weight/rule treatment explicitly forbidden from using the blue or green tokens, and verification greps to confirm the blue token appears in exactly one rule. The /tmp scratch file carries all three nav states side by side, so the front-page case is visually proven to have no marked link before the contract is applied to any real page.

## Verification

Open /tmp/nav-check.html at 380px and 1280px: the first nav shows no marked link, the second marks Docs, the third marks Examples, and in all three the nav holds exactly three links with no Home link present. Confirm the nav wraps rather than overflows at 380px and that the document body does not scroll horizontally, satisfying nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout. Run `grep -c 'wordmark-blue' styles.css` and confirm the token is referenced in exactly one rule. Run `grep -niE 'svg|icon|hamburger|dropdown' styles.css` and expect no matches. Toggle the OS between light and dark appearance and confirm the wordmark, version, nav links, and the current-section indicator all remain legible, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. Confirm the nav section of styles.css contains the canonical markup contract as a comment block. Re-extract the text of all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/ — expect zero differences, as this phase touches no HTML.

**Non-functional acceptance** (deterministic, from the stack spec):

- `nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout`: Pages remain fully readable and navigable on narrow viewports without horizontal breakage of the overall layout — delivered by stylesheet
- `nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes`: Text and code remain readable at sufficient contrast in both light and dark reading schemes — delivered by stylesheet
- `nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages`: The shared visual presentation can be updated once and take effect consistently across all pages — delivered by stylesheet


## References

- [ARIA aria-current attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-current)
- [CSS Flexible Box Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout)
- [WCAG 2.1 SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)
