import re
from config import Token, regex

# --- LEXER / TOKENIZER ---
def tokenize(text):
    pos = 0

    while pos < len(text):
        match = re.match(regex, text[pos:])

        if not match:
            pos += 1
            continue

        kind, value = match.lastgroup, match.group()

        if kind != 'WS':
            yield Token(kind, value)

        pos += len(value)