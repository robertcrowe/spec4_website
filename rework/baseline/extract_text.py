#!/usr/bin/env python3
"""Extract the rendered text of an HTML page.

Local verification aid for the rework round. Never served, never referenced by
any page, no third-party dependencies -- Python 3 standard library only.

Usage:  python3 extract_text.py <path-to-html>

Discards <head>, <script> and <style> contents entirely. Emits the body's text
nodes, one text block per line, with runs of whitespace collapsed to a single
space. Blank blocks are dropped.
"""

import sys
from html.parser import HTMLParser

SKIP_TAGS = {"script", "style", "head"}
# Void elements never emit an end tag, so they must not push onto the stack.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        if self.skip_depth or tag in SKIP_TAGS:
            self.skip_depth += 1

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.blocks.append(text)


def extract(path):
    with open(path, "r", encoding="utf-8") as handle:
        source = handle.read()
    parser = TextExtractor()
    parser.feed(source)
    parser.close()
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
