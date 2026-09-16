# spec4.ai register

Rules for every page on spec4.ai. Every build task follows this file. The pages themselves are the copy: edits are made in the HTML directly, and a build task changes only what it names.

## Copy

1. Use the supplied copy verbatim: headings, order, tables, code blocks, and paragraphs. Do not rewrite, shorten, reorder, or add.
2. Every term in backticks renders in monospace.
3. Oxford commas are already in the copy; keep them.
4. Nothing is added that isn't in the copy: no taglines, no calls to action, no summary boxes, no "learn more" links, no alt text that editorialises.

## Markup

5. Semantic HTML: one `<nav>`, `<main>`, `<h1>`–`<h3>` in order, real `<table>` with `<thead>`, `<pre><code>` for code blocks and excerpts, `<figure>`/`<figcaption>` for screenshots. No layout `<div>`s where an element exists for the purpose. The look is applied later as CSS, so the markup must not encode a look.
6. Until the look pass, pages use the site's existing stylesheet as is. Do not add styling beyond what §2 needs. Do not port styles from the Spec4 app.

## Look (applies at the look pass; read now so the markup doesn't fight it)

The site is consistent with the Spec4 app in its brand elements and is a reading layout otherwise. It does not reproduce the app's UI.

7. **Consistent with the app:** the `Spec4` wordmark; the app's green as the single accent (`#39FF14`, or the variable the app defines); dark background; monospace for every path, filename, command, model name, and figure; text-only nav; no decoration.
8. **The site's own:** typography scale, measure (about 70 characters), line height, section spacing, and table styling for reading rather than scanning. Serif prose — a system stack, Charter first, Georgia fallback; no font files. Left-aligned. *(Amended 2026-09-15: was "Sans-serif prose". The design round settled on a serif and the approved mock ships one.)*
9. Tables: thin rules, dim header, no zebra striping; on narrow viewports they scroll horizontally and never break the layout.
10. Code blocks and excerpts are plain bordered panels. No window chrome, no traffic-light dots, no titlebar.
11. Screenshots of the app appear in the app's own look, with the caption the copy supplies. They are the only place the app's UI appears.

## Not on any page

12. No emoji, icons, or icon fonts. Links are text, including the GitHub link.
13. No images except real screenshots of the app or real artifacts.
14. No gradients, grid backgrounds, badges, pills, kickers, or eyebrow labels.
15. No animation, fade-ins, scroll effects, or decorative motion.
16. No CTA banners, buttons styled as hero actions, or "Get Started" buttons in the nav.
17. No second accent colour. No blue, except in the Spec4 wordmark, where it is the app's.
18. No analytics, no external fonts beyond what the existing pages already load, no JavaScript beyond what the existing pages already load.

## Nav (every page)

19. Text links: `Docs · Examples · GitHub`, current section marked. `Examples` → `/bws4/`; `GitHub` → `https://github.com/robertcrowe/spec4`. The `Spec4` wordmark links to `/`. Version `1.5.0` in monospace. How it is laid out is the look pass's decision; the markup is one `<nav>` with those links.

## Links to pages that don't exist yet

20. Copy marks these with ▸. Render as plain text, not a link, with an HTML comment beside it giving the intended path. Do not create placeholder pages.

## Before finishing any task

21. Open the page at desktop and at ~380px width.
22. Links resolve; no unclosed tags.
23. Show the full page HTML and any stylesheet diff. Do not commit or push.
24. Cross-links. On each page, the first mention of an agent links to its page, the first mention of an artifact filename links to `/docs/artifacts/`, and the first mention of rounds, settings, the front page's subject, or Built With Spec4 links to that page. Later mentions on the same page are plain. No links inside code blocks, tables of verbatim data, quoted excerpts, headings, or the nav. A page never links to itself. A link's text is the term as written; nothing is reworded to make a link.