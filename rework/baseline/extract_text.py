#!/usr/bin/env python3
"""Extract the rendered text of an HTML page.

Local verification aid for the rework round. Never served, never referenced by
any page, no third-party dependencies -- Python 3 standard library only.

Usage:  python3 extract_text.py <path-to-html>

Discards <head>, <script> and <style> contents entirely. Emits one line per
block-level element, with the text of any inline elements inside it joined as
the reader sees it and runs of whitespace collapsed to a single space. Blank
blocks are dropped.

Segmentation note (changed in Phase 6). This script originally emitted one line
per HTML text node, which made it sensitive to markup that does not change what
a reader sees: splitting `Spec4` into `<span>Spec</span><span>4</span>` for the
wordmark's two-colour treatment produced two lines out of one, and separate
lines for inline links inside a paragraph. Text is now accumulated across
inline elements and flushed at block boundaries, so the output tracks rendered
text rather than markup structure. The baselines under text/ were regenerated
with this version from the untouched pre-round snapshots in html/, and the full
word sequence was verified unchanged against the previous output.
"""

import sys
from html.parser import HTMLParser

SKIP_TAGS = {"script", "style", "head"}

# Void elements never emit an end tag, so they must not push onto the stack.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Text inside these is part of the surrounding line, as it is on screen.
INLINE_TAGS = {
    "a", "abbr", "b", "bdi", "bdo", "cite", "code", "data", "del", "dfn",
    "em", "i", "ins", "kbd", "mark", "q", "s", "samp", "small", "span",
    "strong", "sub", "sup", "time", "u", "var",
}


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.buffer = []
        self.blocks = []

    def flush(self):
        text = " ".join("".join(self.buffer).split())
        if text:
            self.blocks.append(text)
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            # <br> ends the visual line; other void elements are not text.
            if tag == "br" and not self.skip_depth:
                self.flush()
            return
        if self.skip_depth or tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if tag not in INLINE_TAGS:
            self.flush()

    def handle_startendtag(self, tag, attrs):
        if tag == "br" and not self.skip_depth:
            self.flush()

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if tag not in INLINE_TAGS:
            self.flush()

    def handle_data(self, data):
        if self.skip_depth:
            return
        self.buffer.append(data)


def extract(path):
    with open(path, "r", encoding="utf-8") as handle:
        source = handle.read()
    parser = TextExtractor()
    parser.feed(source)
    parser.close()
    parser.flush()
    return parser.blocks


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: extract_text.py <path-to-html>\n")
        return 2
    for block in extract(argv[1]):
        print(block)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
