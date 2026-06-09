import pytest

from src.transpilador.parser.analisador import Parser
from src.transpilador.parser.ast_nodes import (
    AssignNode,
    IfNode,
    PrintNode,
    ProgramNode,
    ReadNode,
    VarDeclNode,
    WhileNode,
)
from src.transpilador.lexer.lexer import tokenize


def gerar_ast(codigo: str):
    """Função auxiliar para tokenizar e fazer o parse do código."""

    return Parser(tokens=list(tokenize(codigo))).parse_program()


def test_parser_estrutura_basica_programa():
    # codigo = "ohjelma loppu"
    # tokens = list(tokenize(codigo))
    # parser = Parser(tokens)

    ast = gerar_ast("ohjelma loppu")

    assert isinstance(ast, ProgramNode)
    assert len(ast.body) == 0


def test_parser_erro_falta_ohjelma():
    codigo = "kokonaisluku x. loppu"

    # O pytest verifica se a exceção SyntaxError é levantada com a mensagem correta
    with pytest.raises(
        SyntaxError, match="O programa deve começar com a palavra reservada 'ohjelma'."
    ):
        gerar_ast(codigo)


def test_parser_erro_falta_loppu():
    codigo = "ohjelma kokonaisluku x."

    with pytest.raises(
        SyntaxError, match="O programa deve terminar com a palavra reservada 'loppu'."
    ):
        gerar_ast(codigo)


def test_parser_erro_falta_ponto_kirjoita():
    codigo = 'ohjelma kirjoita("Erro sem ponto") loppu'

    with pytest.raises(SyntaxError, match="Esperado um ponto '.' no final"):
        gerar_ast(codigo)


def test_parser_declaracao_variavel_todos_os_tipos():
    # codigo = "ohjelma kokonaisluku a. desimaali b. merkkijono c. totuusarvo d. loppu"
    # tokens = list(tokenize(codigo))
    # parser = Parser(tokens)

    ast = gerar_ast(
        "ohjelma kokonaisluku a. desimaali b. merkkijono c. totuusarvo d. loppu"
    )

    node_all_decl = ast.body

    assert node_all_decl[0].var_type == "TYPE_INT"
    assert node_all_decl[1].var_type == "TYPE_DEC"
    assert node_all_decl[2].var_type == "TYPE_STR"
    assert node_all_decl[3].var_type == "TYPE_BOOL"


def test_parser_declaracao_variavel_multiplas():
    # codigo = "ohjelma kokonaisluku x, y. loppu"
    # tokens = list(tokenize(codigo))
    # parser = Parser(tokens)

    ast = gerar_ast("ohjelma kokonaisluku x, y. loppu")

    node_decl_mult = ast.body[0]

    assert isinstance(node_decl_mult, VarDeclNode)
    assert node_decl_mult.var_type == "TYPE_INT"
    assert node_decl_mult.variables == ["x", "y"]


def test_parser_atribuicao_literal():
    # codigo = "ohjelma x := 10. loppu"
    # tokens = list(tokenize(codigo))
    # parser = Parser(tokens)

    ast = gerar_ast("ohjelma x := 10. loppu")

    node_assign = ast.body[0]

    assert isinstance(node_assign, AssignNode)
    assert node_assign.var_name == "x"
    assert node_assign.value == "10"


def test_parser_atribuicao_expressao_aritmetica():
    # codigo = "ohjelma x := 2 + 2. loppu"
    # tokens = list(tokenize(codigo))
    # parser = Parser(tokens)

    ast = gerar_ast("ohjelma x := 2 + 2. loppu")

    node_assign_exp = ast.body[0]

    assert isinstance(node_assign_exp, AssignNode)
    assert node_assign_exp.var_name == "x"
    assert node_assign_exp.value == "2 + 2"


def test_parser_comando_kirjoita():
    # codigo = 'ohjelma kirjoita("Hello, world"). loppu'
    # tokens = list(tokenize(codigo))
    # parser = Parser(tokens)

    ast = gerar_ast('ohjelma kirjoita("Hello, world"). loppu')

    assert len(ast.body) == 1

    node_print = ast.body[0]

    assert isinstance(node_print, PrintNode)
    assert node_print.value == '"Hello, world"'


def test_parser_comando_lue():
    ast = gerar_ast("ohjelma lue(name). loppu")

    node_read = ast.body[0]

    assert isinstance(node_read, ReadNode)
    assert node_read.var_name == "name"


def test_parser_comando_jos():
    ast = gerar_ast("ohjelma jos (x == 1) { kirjoita(x). } loppu")

    node_if = ast.body[0]

    assert isinstance(node_if, IfNode)
    assert node_if.condition == "x == 1"
    assert len(node_if.body) == 1
    assert isinstance(node_if.body[0], PrintNode)
    assert node_if.body[0].value == "x"


def test_parser_comando_kunnes():
    ast = gerar_ast("ohjelma kunnes (x != 0) { x := x - 1. } loppu")

    node_while = ast.body[0]

    assert isinstance(node_while, WhileNode)
    assert node_while.condition == "x != 0"
    assert len(node_while.body) == 1
    assert isinstance(node_while.body[0], AssignNode)
    assert node_while.body[0].var_name == "x"
    assert node_while.body[0].value == "x - 1"


def test_parser_multiplos_comandos():
    ast = gerar_ast("ohjelma kokonaisluku x. x := 5. kirjoita(x). loppu")

    node = ast.body

    assert len(node) == 3
    assert isinstance(node[0], VarDeclNode)
    assert isinstance(node[1], AssignNode)
    assert isinstance(node[2], PrintNode)


def test_parser_while_com_if_aninhado():
    ast = gerar_ast("ohjelma kunnes (x != 9) { jos (x == 1) { kirjoita(x). } } loppu")

    node = ast.body
    node_while = node[0]

    assert isinstance(node_while, WhileNode)

    node_if = node_while.body
    assert isinstance(node_if[0], IfNode)
