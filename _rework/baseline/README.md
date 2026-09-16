# Baseline

This directory is the pre-round snapshot of the site as it was authored before
the rework began. Its purpose is narrow and mechanical: to prove that the
*rendered text* of every one of the thirteen styled pages is byte-identical
before and after the round. The round is allowed to change styling, markup
structure, and class names freely; it is not allowed to change a single word a
reader sees. `html/` holds a byte-for-byte copy of each page's HTML as it stood
at the start, `text/` holds the rendered text extracted from those copies, and
`inventory.md` records the page/stub classification and what `styles.css`
contained before Phase 2 replaced it. The text under `rework/*.md` remains the
authoritative source for what each page should say; these `text/` files are the
evidence that the live pages still say it. Nothing here is served, referenced by
any page, or deployed — `extract_text.py` uses only the Python 3 standard
library and adds no dependency to the site.

To check a page, re-extract its text from the live source and diff it against
the baseline. For `/docs/rounds/`, from the repository root:

```
python3 rework/baseline/extract_text.py docs/rounds/index.html | diff - rework/baseline/text/docs-rounds.txt
```

An empty diff (exit status 0) is a pass. Substitute the page's own source path
and its matching `text/` stem for any other page; the stems are listed in the
styled-pages table in `inventory.md`. To sweep all thirteen at once:

```
for f in rework/baseline/html/*.html; do
  n=$(basename "$f" .html)
  python3 rework/baseline/extract_text.py "$f" | diff -q - "rework/baseline/text/$n.txt" || echo "DRIFT: $n"
done
```

Run that sweep against the live source paths rather than `html/` once a later
phase has edited the real pages — `html/` is the frozen original and will always
match.
