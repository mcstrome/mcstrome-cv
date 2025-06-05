from html.parser import HTMLParser
from pathlib import Path


VOID_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
    'meta', 'param', 'source', 'track', 'wbr'
}

class ValidatingHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        # Self-closing tags do not affect the stack
        pass

    def handle_endtag(self, tag):
        if not self.stack:
            self.errors.append(f"Unexpected closing tag: {tag}")
            return
        last = self.stack.pop()
        if last != tag:
            self.errors.append(
                f"Mismatched closing tag: {tag} (expected {last})"
            )

    def close(self):
        super().close()
        if self.stack:
            self.errors.append(f"Unclosed tags: {self.stack}")


def test_index_html_parses_cleanly():
    html_path = Path(__file__).resolve().parents[1] / 'index.html'
    parser = ValidatingHTMLParser()
    with html_path.open('r', encoding='utf-8') as f:
        parser.feed(f.read())
    parser.close()
    assert not parser.errors, f"HTML parse errors: {parser.errors}"
