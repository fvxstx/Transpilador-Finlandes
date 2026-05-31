from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str


DICTIONARY = {
    "COMMANDS": {
        "ohjelma": "Início do programa",
        "loppu": "Fim do programa",
        "jos": "If",
        "muuten": "Else",
        "kunnes": "While",
        "lue": "Input",
        "kirjoita": "Print",
    },
    "TYPES": {
        "kokonaisluku": "Inteiro",
        "desimaali": "Decimal",
        "merkkijono": "Texto",
        "totuusarvo": "Booleano",
    },
    "OPERATORS": {
        ":=": "Atribuição",
        "==": "Igual a",
        "!=": "Diferente",
        "+": "Soma",
        "-": "Subtração",
        "*": "Multiplicação",
        "/": "Divisão",
    },
}

TOKEN_SPEC = [
    ("PROGRAM", r"ohjelma"),
    ("ENDPROG", r"loppu"),
    ("TYPE_BOOL", r"totuusarvo"),
    ("TRUE", r"tosi"),
    ("FALSE", r"epätosi"),
    ("TYPE_INT", r"kokonaisluku"),
    ("TYPE_DEC", r"desimaali"),
    ("TYPE_STR", r"merkkijono"),
    ("IF", r"jos"),
    ("ELSE", r"muuten"),
    ("WHILE", r"kunnes"),
    ("READ", r"lue"),
    ("WRITE", r"kirjoita"),
    ("NUMBER_DEC", r"\d+\.\d+"),
    ("NUMBER_INT", r"\d+"),
    ("STRING", r'"[^"]*"'),
    ("ID", r"[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*"),
    ("ASSIGN", r":="),
    ("OP_REL", r"[<>!=]=|[<>]|=="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("COMMA", r","),
    ("DOT", r"\."),
    ("WS", r"\s+"),
]
