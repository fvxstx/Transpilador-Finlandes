import re

from config import TOKEN_SPEC, Token

regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)


def tokenize(text):
    pos = 0

    while pos < len(text):
        match = re.match(regex, text[pos:])

        if not match:
            pos += 1
            continue

        kind, value = match.lastgroup, match.group()

        if kind is not None and kind != "WS":
            yield Token(kind, value)

        pos += len(value)
