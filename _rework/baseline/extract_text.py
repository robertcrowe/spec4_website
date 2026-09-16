#!/usr/bin/env python3
"""Extract the rendered text of an HTML page.

Local verification aid for the rework round. Never served, never referenced by
any page, no third-party dependencies -- Python 3 standard library only.

Usage:  python3 extract_text.py <path-to-html>
        python3 extract_text.py --check-balance <path-to-html> [...]

The --check-balance mode (added in Phase 7) reports any tag closed out of order
or left open at end of file. Void elements are ignored, per the WHATWG list.

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

import pathlib
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


class BalanceChecker(HTMLParser):
    """Pushes on start tags, pops on end tags, ignoring void elements."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> with nothing open")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # Closed out of order: report against whatever was actually open.
        if any(t == tag for t, _ in self.stack):
            open_tag, open_pos = self.stack[-1]
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes out of order; "
                f"<{open_tag}> opened at line {open_pos[0]} is still open")
            while self.stack and self.stack[-1][0] != tag:
                self.stack.pop()
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> was never opened")

    def report(self):
        for tag, pos in self.stack:
            self.errors.append(f"line {pos[0]}: <{tag}> left open at end of file")
        return self.errors


def check_balance(paths):
    failed = 0
    for path in paths:
        checker = BalanceChecker()
        checker.feed(pathlib.Path(path).read_text(encoding="utf-8"))
        checker.close()
        errors = checker.report()
        if errors:
            failed = 1
            print(f"{path}: UNBALANCED")
            for e in errors:
                print(f"    {e}")
        else:
            print(f"{path}: balanced")
    return failed


def main(argv):
    if len(argv) >= 3 and argv[1] == "--check-balance":
        return check_balance(argv[2:])
    if len(argv) != 2:
        sys.stderr.write("usage: extract_text.py [--check-balance] <path-to-html>\n")
        return 2
    for block in extract(argv[1]):
        print(block)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
