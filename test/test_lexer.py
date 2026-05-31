import pytest

from lexer import tokenize


def test_tokeniza_palavras_reservadas():
    codigo = "ohjelma loppu jos muuten kunnes lue kirjoita tosi epätosi"
    tokens = list(tokenize(codigo))

    esperado = [
        ("PROGRAM", "ohjelma"),
        ("ENDPROG", "loppu"),
        ("IF", "jos"),
        ("ELSE", "muuten"),
        ("WHILE", "kunnes"),
        ("READ", "lue"),
        ("WRITE", "kirjoita"),
        ("TRUE", "tosi"),
        ("FALSE", "epätosi"),
    ]

    resultado = [(token.type, token.value) for token in tokens]

    assert resultado == esperado


def test_tokeniza_tipos():
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


def test_tokeniza_operadores():
    codigo = ":= + - * / == != > < >= <="
    tokens = list(tokenize(codigo))

    esperado = [
        ("ASSIGN", ":="),
        ("PLUS", "+"),
        ("MINUS", "-"),
        ("MUL", "*"),
        ("DIV", "/"),
        ("OP_REL", "=="),
        ("OP_REL", "!="),
        ("OP_REL", ">"),
        ("OP_REL", "<"),
        ("OP_REL", ">="),
        ("OP_REL", "<="),
    ]

    resultado = [(token.type, token.value) for token in tokens]

    assert resultado == esperado


def test_tokeniza_pontuacoes():
    codigo = "( ) { } , ."
    tokens = list(tokenize(codigo))

    esperado = [
        ("LPAREN", "("),
        ("RPAREN", ")"),
        ("LBRACE", "{"),
        ("RBRACE", "}"),
        ("COMMA", ","),
        ("DOT", "."),
    ]

    resultado = [(token.type, token.value) for token in tokens]

    assert resultado == esperado


def test_tokeniza_literais_e_identificadores():
    codigo = '123 45.55 "Hello, world" my_foo'
    tokens = list(tokenize(codigo))

    esperado = [
        ("NUMBER_INT", "123"),
        ("NUMBER_DEC", "45.55"),
        ("STRING", '"Hello, world"'),
        ("ID", "my_foo"),
    ]

    resultado = [(token.type, token.value) for token in tokens]

    assert resultado == esperado


def test_tokeniza_caractere_invalido():
    codigo = "ohjelma @ loppu"  # O @ não faz parte do nosso TOKEN_SPEC

    with pytest.raises(ValueError) as err:
        list(tokenize(codigo))

    assert "Caractere inválido: @" in str(err.value)


def test_identificador_com_prefixo_de_keyword():
    codigo = "josebahia loppuminha tosivida"
    tokens = list(tokenize(codigo))

    esperado = [("ID", "josebahia"), ("ID", "loppuminha"), ("ID", "tosivida")]

    resultado = [(token.type, token.value) for token in tokens]

    assert resultado == esperado
