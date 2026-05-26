from lexer import tokenize


def test_tokeniza_palavras_reservadas():
    codigo = "ohjelma jos tosi loppu"
    tokens = list(tokenize(codigo))

    esperado = [
        ("PROGRAM", "ohjelma"),
        ("ENDPROG", "loppu"),
        ("IF", "jos"),
        ("ELSE", "muuten"),
        ("TRUE", "tosi"),
        ("WHILE", "kunners"),
        ("READ", "lue"),
        ("WRITE", "kirjoita"),
        ("TRUE", "tosi"),
        ("FALSE", "epätosi"),
    ]

    resultado = [(token.type, token.value) for token in tokens]

    assert resultado == esperado


def test_tokeniza_operadores():
    codigo = "kokonaisluku desimaali merkkijono totuusarvo"
    tokens = list(tokenize(codigo))

    esperado = [
        ("TYPE_INT", "kokonaisluku"),
        ("TYPE_DEC", "desimaali"),
        ("TYPE_STR", "merkkijono"),
        ("TYPE_BOOL", "totuusarvo"),
    ]

    resultado = [(token.type, token.value) for token in tokens]

    assert resultado == esperado


def test_tokeniza_tipos(): ...
