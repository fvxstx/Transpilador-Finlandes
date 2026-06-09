import pytest

from src.transpilador.parser.analisador import Parser
from src.transpilador.codegen.gerador import PythonCodeGenerator
from src.transpilador.lexer.lexer import tokenize


def gerar_codigo_python(codigo_finlandes: str) -> str:
    """Função auxiliar: pega o código finlandês e devolve a string em python."""

    tokens = list(tokenize(codigo_finlandes))
    ast = Parser(tokens).parse_program()
    gerador = PythonCodeGenerator()

    return gerador.generate(ast)


def test_gerador_programa_vazio():
    codigo = "ohjelma loppu"
    esperado = "def run_program():\n\nrun_program()"

    assert gerar_codigo_python(codigo) == esperado


def test_gerador_comando_print():
    codigo = "ohjelma kirjoita(10). loppu"
    esperado = "def run_program():\n    print(10)\n\nrun_program()"

    assert gerar_codigo_python(codigo) == esperado


def test_gerador_declaracao_variaveis_valores_padrao():
    codigo = "ohjelma kokonaisluku a. desimaali b. merkkijono c. totuusarvo d. loppu"
    esperado = (
        "def run_program():\n"
        "    a = 0\n"
        "    b = 0.0\n"
        '    c = ""\n'
        "    d = False\n"
        "\n"
        "run_program()"
    )

    assert gerar_codigo_python(codigo) == esperado


def test_gerador_atribuicao_booleana():
    codigo = "ohjelma x := tosi. y := epätosi. loppu"
    esperado = "def run_program():\n    x = True\n    y = epäTrue\n\nrun_program()"

    assert gerar_codigo_python(codigo) == esperado


def test_gerador_comando_leitura():
    codigo = "ohjelma lue(Lebron). loppu"
    esperado = (
        "def run_program():\n    Lebron = terminal_input('Lebron')\n\nrun_program()"
    )

    assert gerar_codigo_python(codigo) == esperado
