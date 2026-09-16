---
{
  "phase_number": 7,
  "total_phases": 7,
  "phase_title": "Verification Sweep & Exclusion Audit",
  "phase_summary": "Prove the finished site against every acceptance criterion: no horizontal body scroll at 380px or 1280px on any page, copy byte-identical to the Phase 1 baseline, readable light and dark schemes, readable with the stylesheet disabled, no excluded decoration or third-party request anywhere, and the ten redirect stubs still carrying no stylesheet link.",
  "features": [
    {
      "id": "unified_stylesheet",
      "role": "extended",
      "scope_note": "Final cross-page conformance pass — audits and corrects the shared presentation against every success criterion and the standing exclusion list; closes the feature."
    }
  ],
  "capabilities": [],
  "tech_stack_spec": {
    "dependencies": [],
    "configurations": "No new files are added to the site. Any correction made in this phase is a targeted edit to styles.css or to a page's markup, never a new page-specific stylesheet or inline style. Checks are mechanical and run against the local static server; the W3C Nu Html Checker remains a developer habit outside this plan and is not a step here."
  },
  "instructions": [
    "Serve the repository root with the local static server and open all thirteen styled pages in turn. Work from rework/baseline/inventory.md so no page is missed.",
    "Mechanical markup check, per page: confirm there are no unclosed or mismatched tags. Extend rework/baseline/extract_text.py with a standard-library tag-balance check — an html.parser subclass that pushes on start tags, pops on end tags, ignores the HTML void elements, and reports any tag closed out of order or left open at EOF — and run it over all thirteen pages. Every page must report a balanced tree.",
    "Mechanical link check: collect every internal href and src across the thirteen pages and confirm each one resolves to a file that exists in the repository — including the ten redirect-stub paths, /styles.css, both .woff2 files, the favicon, and every image. Report any target that does not resolve and fix the reference, not the target.",
    "Mechanical viewport check: for each of the thirteen pages, at viewport widths of exactly 380px and 1280px, confirm `document.documentElement.scrollWidth <= window.innerWidth` in the browser console. Every page must pass at both widths. Note that this console expression is a verification aid typed into devtools — no script is added to any page.",
    "Where a page fails the viewport check, identify the offending element and fix it inside the component that owns it — a missing `.table-wrap`, a code line escaping its panel, an image without max-width. Never fix an overflow by adding overflow-x: hidden to html, body, or main; that rule was deliberately removed in Phase 2 and must not return.",
    "Copy byte-identity: re-extract all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/. The diff must be empty across all thirteen. A non-empty diff is a blocking failure — revert the markup change that caused it.",
    "Stub integrity: run `grep -rl 'http-equiv=\"refresh\"' --include=index.html .` and confirm it still returns the same ten paths recorded in the Phase 1 baseline, then confirm none of those ten contains a stylesheet link, a font reference, or any new markup. The stubs are untouched by this round and must remain twelve-line redirect documents.",
    "Dark-scheme audit: switch the operating system between light and dark appearance and walk all thirteen pages in both. Confirm body text, muted text, nav links, the current-section mark, table rules, code panel text, and figure captions are all legible in both, and that no page shows a color that failed to swap because it was written as a literal rather than a token.",
    "Contrast audit: measure the contrast ratio of primary text on background and muted text on background in both schemes, plus code panel text on the panel tint in both schemes, and confirm each meets 4.5:1 per WCAG 2.1 SC 1.4.3.",
    "No-stylesheet readability: disable CSS in the browser and load the front page, the docs index, and bws4. Confirm each remains readable as a plain document with a sensible heading hierarchy and reading order, and that no content is hidden or made meaningless by the absence of styles.",
    "Exclusion audit: confirm no icon, card shape, hero banner, shadow, gradient, animation, second accent color, or analytics indicator appears anywhere on the site. Run `grep -niE 'shadow|gradient|animation|transition|transform|@keyframes|border-radius' styles.css` and `grep -rniE 'analytics|gtag|plausible|<svg|<script' --include=index.html .` and expect no matches from either.",
    "Blue audit: confirm the wordmark's two-color treatment is the only place blue appears on the site — walk the thirteen pages visually in both schemes, and confirm the --wordmark-blue token is referenced by exactly one rule in styles.css.",
    "Consistency audit: confirm all thirteen pages share identical navigation placement, identical wordmark treatment, and identical typography, and that this is achieved by the shared stylesheet rather than by page-specific overrides — confirm the page-specific overrides section of styles.css is empty or contains only rules that could not be expressed as shared components, each with a comment explaining why.",
    "Resource audit: load each of the thirteen pages with the Network panel open and confirm the requests are exactly the page's own HTML, /styles.css, the two fonts, and that page's images — nothing else, from no other host.",
    "Record the outcome of every check in `rework/baseline/verification.md`: one line per page for the 380px and 1280px results, one line per audit, and an explicit statement of the ten stubs' continued stylesheet-free state. Note any copy drift previously recorded in inventory.md as still outstanding, so it carries into a future round rather than being lost.",
    "After this phase is complete and all verification passes, create the set-completion marker so Spec4 can detect this phase set is implemented: `touch .spec4/v1/IMPLEMENTED`"
  ],
  "risk_assessment": {
    "potential_bottlenecks": "The dominant risk in a final sweep is the shortcut fix: an agent that finds an overflow at 380px on one page reaches for a page-specific override or a body-level overflow-x: hidden, which makes the check pass while destroying the single-stylesheet guarantee and hiding the real defect. A second risk is partial coverage — auditing three representative pages and declaring thirteen done — which is exactly how one page ends up with different typography from the rest. A third is treating an audit failure as a reason to edit copy, which would break the byte-identity guarantee at the last moment.",
    "mitigation_strategy": "Every check is specified as running across all thirteen pages driven from the Phase 1 inventory, and the results are written per page into rework/baseline/verification.md, so partial coverage is visible in the artifact rather than hidden in a summary claim. Overflow fixes are explicitly required to be made inside the owning component, with the body-level hidden rule named as forbidden. Copy byte-identity is re-checked against the baseline as its own blocking step, and the instruction for any discovered copy drift is to record it, never to edit the text. The W3C Nu Html Checker is deliberately excluded in favour of mechanical tag-balance, link-resolution, and scrollWidth checks so the phase's pass condition is reproducible in a fresh session."
  },
  "verification": "All thirteen pages pass the tag-balance check with no unclosed or mismatched tags, and every internal link and asset reference resolves to a file present in the repository. For all thirteen pages at both 380px and 1280px, `document.documentElement.scrollWidth <= window.innerWidth` holds, with wide tables and code samples scrolling only inside their own containers — satisfying nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout. Re-extracting all thirteen pages with rework/baseline/extract_text.py and diffing against rework/baseline/text/ yields zero differences. `grep -rl 'http-equiv=\"refresh\"' --include=index.html .` returns the same ten stub paths as the Phase 1 baseline, and none of those ten contains a stylesheet link. Primary and muted text on background, and code text on panel tint, meet 4.5:1 in both light and dark schemes, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. With CSS disabled, the front page, docs index, and bws4 remain readable. The exclusion greps return no matches and no page requests any resource beyond its own HTML, /styles.css, the two fonts, and its own images — satisfying nfr_every_page_loads_and_renders_correctly_without_requiring_any_script_to_run, nfr_pages_load_quickly_even_on_slow_connections__given_they_contain_no_scripts__media_playback__or_heavy_assets, and nfr_the_site_collects_no_analytics_or_tracking_information_about_readers. All thirteen pages share identical nav placement, wordmark treatment, and typography from the one stylesheet with an effectively empty page-specific overrides section, satisfying nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages. rework/baseline/verification.md records every result.",
  "references": [
    {
      "standard": "WCAG 2.1 SC 1.4.3 Contrast (Minimum)",
      "url": "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum"
    },
    {
      "standard": "prefers-color-scheme (CSS media feature)",
      "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme"
    },
    {
      "standard": "WHATWG HTML Living Standard (void elements)",
      "url": "https://html.spec.whatwg.org/multipage/syntax.html#void-elements"
    },
    {
      "standard": "WHATWG HTML Living Standard (meta http-equiv=refresh, used by the redirect stubs)",
      "url": "https://html.spec.whatwg.org/multipage/semantics.html#attr-meta-http-equiv-refresh"
    },
    {
      "standard": "Sitemaps protocol",
      "url": "https://www.sitemaps.org/protocol.html"
    },
    {
      "standard": "GitHub Pages",
      "url": "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"
    },
    {
      "standard": "Python html.parser (standard library, used by the local verification script)",
      "url": "https://docs.python.org/3/library/html.parser.html"
    }
  ]
}
---

# Phase 7 of 7: Verification Sweep & Exclusion Audit

Prove the finished site against every acceptance criterion: no horizontal body scroll at 380px or 1280px on any page, copy byte-identical to the Phase 1 baseline, readable light and dark schemes, readable with the stylesheet disabled, no excluded decoration or third-party request anywhere, and the ten redirect stubs still carrying no stylesheet link.

## Feature Specifications

These specifications are authoritative for this phase. Implement to them; the instructions below tell you how and in what order.

### Unified_Stylesheet — product feature — extended in this phase

*Scope for this phase: Final cross-page conformance pass — audits and corrects the shared presentation against every success criterion and the standing exclusion list; closes the feature.*

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

**Configurations:** No new files are added to the site. Any correction made in this phase is a targeted edit to styles.css or to a page's markup, never a new page-specific stylesheet or inline style. Checks are mechanical and run against the local static server; the W3C Nu Html Checker remains a developer habit outside this plan and is not a step here.

**Approved stack for this phase's declared work** (deterministic, from the stack spec):

- pages (persistence) — serves `unified_stylesheet`
- stylesheet (persistence) — serves `unified_stylesheet`
- fonts (persistence): two weights of JetBrains Mono, .woff2 only, for monospace/code/nav/version text; the reading face is a system font stack with no files — serves `unified_stylesheet`
- images (persistence) — serves `unified_stylesheet`

## Instructions

1. Serve the repository root with the local static server and open all thirteen styled pages in turn. Work from rework/baseline/inventory.md so no page is missed.
2. Mechanical markup check, per page: confirm there are no unclosed or mismatched tags. Extend rework/baseline/extract_text.py with a standard-library tag-balance check — an html.parser subclass that pushes on start tags, pops on end tags, ignores the HTML void elements, and reports any tag closed out of order or left open at EOF — and run it over all thirteen pages. Every page must report a balanced tree.
3. Mechanical link check: collect every internal href and src across the thirteen pages and confirm each one resolves to a file that exists in the repository — including the ten redirect-stub paths, /styles.css, both .woff2 files, the favicon, and every image. Report any target that does not resolve and fix the reference, not the target.
4. Mechanical viewport check: for each of the thirteen pages, at viewport widths of exactly 380px and 1280px, confirm `document.documentElement.scrollWidth <= window.innerWidth` in the browser console. Every page must pass at both widths. Note that this console expression is a verification aid typed into devtools — no script is added to any page.
5. Where a page fails the viewport check, identify the offending element and fix it inside the component that owns it — a missing `.table-wrap`, a code line escaping its panel, an image without max-width. Never fix an overflow by adding overflow-x: hidden to html, body, or main; that rule was deliberately removed in Phase 2 and must not return.
6. Copy byte-identity: re-extract all thirteen pages with rework/baseline/extract_text.py and diff against rework/baseline/text/. The diff must be empty across all thirteen. A non-empty diff is a blocking failure — revert the markup change that caused it.
7. Stub integrity: run `grep -rl 'http-equiv="refresh"' --include=index.html .` and confirm it still returns the same ten paths recorded in the Phase 1 baseline, then confirm none of those ten contains a stylesheet link, a font reference, or any new markup. The stubs are untouched by this round and must remain twelve-line redirect documents.
8. Dark-scheme audit: switch the operating system between light and dark appearance and walk all thirteen pages in both. Confirm body text, muted text, nav links, the current-section mark, table rules, code panel text, and figure captions are all legible in both, and that no page shows a color that failed to swap because it was written as a literal rather than a token.
9. Contrast audit: measure the contrast ratio of primary text on background and muted text on background in both schemes, plus code panel text on the panel tint in both schemes, and confirm each meets 4.5:1 per WCAG 2.1 SC 1.4.3.
10. No-stylesheet readability: disable CSS in the browser and load the front page, the docs index, and bws4. Confirm each remains readable as a plain document with a sensible heading hierarchy and reading order, and that no content is hidden or made meaningless by the absence of styles.
11. Exclusion audit: confirm no icon, card shape, hero banner, shadow, gradient, animation, second accent color, or analytics indicator appears anywhere on the site. Run `grep -niE 'shadow|gradient|animation|transition|transform|@keyframes|border-radius' styles.css` and `grep -rniE 'analytics|gtag|plausible|<svg|<script' --include=index.html .` and expect no matches from either.
12. Blue audit: confirm the wordmark's two-color treatment is the only place blue appears on the site — walk the thirteen pages visually in both schemes, and confirm the --wordmark-blue token is referenced by exactly one rule in styles.css.
13. Consistency audit: confirm all thirteen pages share identical navigation placement, identical wordmark treatment, and identical typography, and that this is achieved by the shared stylesheet rather than by page-specific overrides — confirm the page-specific overrides section of styles.css is empty or contains only rules that could not be expressed as shared components, each with a comment explaining why.
14. Resource audit: load each of the thirteen pages with the Network panel open and confirm the requests are exactly the page's own HTML, /styles.css, the two fonts, and that page's images — nothing else, from no other host.
15. Record the outcome of every check in `rework/baseline/verification.md`: one line per page for the 380px and 1280px results, one line per audit, and an explicit statement of the ten stubs' continued stylesheet-free state. Note any copy drift previously recorded in inventory.md as still outstanding, so it carries into a future round rather than being lost.
16. After this phase is complete and all verification passes, create the set-completion marker so Spec4 can detect this phase set is implemented: `touch .spec4/v1/IMPLEMENTED`

## Risk Assessment

**Potential bottlenecks:**

The dominant risk in a final sweep is the shortcut fix: an agent that finds an overflow at 380px on one page reaches for a page-specific override or a body-level overflow-x: hidden, which makes the check pass while destroying the single-stylesheet guarantee and hiding the real defect. A second risk is partial coverage — auditing three representative pages and declaring thirteen done — which is exactly how one page ends up with different typography from the rest. A third is treating an audit failure as a reason to edit copy, which would break the byte-identity guarantee at the last moment.

**Mitigation strategy:**

Every check is specified as running across all thirteen pages driven from the Phase 1 inventory, and the results are written per page into rework/baseline/verification.md, so partial coverage is visible in the artifact rather than hidden in a summary claim. Overflow fixes are explicitly required to be made inside the owning component, with the body-level hidden rule named as forbidden. Copy byte-identity is re-checked against the baseline as its own blocking step, and the instruction for any discovered copy drift is to record it, never to edit the text. The W3C Nu Html Checker is deliberately excluded in favour of mechanical tag-balance, link-resolution, and scrollWidth checks so the phase's pass condition is reproducible in a fresh session.

## Verification

All thirteen pages pass the tag-balance check with no unclosed or mismatched tags, and every internal link and asset reference resolves to a file present in the repository. For all thirteen pages at both 380px and 1280px, `document.documentElement.scrollWidth <= window.innerWidth` holds, with wide tables and code samples scrolling only inside their own containers — satisfying nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout. Re-extracting all thirteen pages with rework/baseline/extract_text.py and diffing against rework/baseline/text/ yields zero differences. `grep -rl 'http-equiv="refresh"' --include=index.html .` returns the same ten stub paths as the Phase 1 baseline, and none of those ten contains a stylesheet link. Primary and muted text on background, and code text on panel tint, meet 4.5:1 in both light and dark schemes, satisfying nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes. With CSS disabled, the front page, docs index, and bws4 remain readable. The exclusion greps return no matches and no page requests any resource beyond its own HTML, /styles.css, the two fonts, and its own images — satisfying nfr_every_page_loads_and_renders_correctly_without_requiring_any_script_to_run, nfr_pages_load_quickly_even_on_slow_connections__given_they_contain_no_scripts__media_playback__or_heavy_assets, and nfr_the_site_collects_no_analytics_or_tracking_information_about_readers. All thirteen pages share identical nav placement, wordmark treatment, and typography from the one stylesheet with an effectively empty page-specific overrides section, satisfying nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages. rework/baseline/verification.md records every result.

**Non-functional acceptance** (deterministic, from the stack spec):

- `nfr_every_page_loads_and_renders_correctly_without_requiring_any_script_to_run`: Every page loads and renders correctly without requiring any script to run — project-wide acceptance
- `nfr_pages_remain_fully_readable_and_navigable_on_narrow_viewports_without_horizontal_breakage_of_the_overall_layout`: Pages remain fully readable and navigable on narrow viewports without horizontal breakage of the overall layout — delivered by stylesheet
- `nfr_text_and_code_remain_readable_at_sufficient_contrast_in_both_light_and_dark_reading_schemes`: Text and code remain readable at sufficient contrast in both light and dark reading schemes — delivered by stylesheet
- `nfr_the_shared_visual_presentation_can_be_updated_once_and_take_effect_consistently_across_all_pages`: The shared visual presentation can be updated once and take effect consistently across all pages — delivered by stylesheet
- `nfr_the_site_collects_no_analytics_or_tracking_information_about_readers`: The site collects no analytics or tracking information about readers — project-wide acceptance
- `nfr_pages_load_quickly_even_on_slow_connections__given_they_contain_no_scripts__media_playback__or_heavy_assets`: Pages load quickly even on slow connections, given they contain no scripts, media playback, or heavy assets — project-wide acceptance


## References

- [WCAG 2.1 SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)
- [prefers-color-scheme (CSS media feature)](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme)
- [WHATWG HTML Living Standard (void elements)](https://html.spec.whatwg.org/multipage/syntax.html#void-elements)
- [WHATWG HTML Living Standard (meta http-equiv=refresh, used by the redirect stubs)](https://html.spec.whatwg.org/multipage/semantics.html#attr-meta-http-equiv-refresh)
- [Sitemaps protocol](https://www.sitemaps.org/protocol.html)
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Python html.parser (standard library, used by the local verification script)](https://docs.python.org/3/library/html.parser.html)
