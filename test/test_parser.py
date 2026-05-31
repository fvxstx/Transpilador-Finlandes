from front.analisador import Parser
from front.ast_nodes import PrintNode, ProgramNode, VarDeclNode
from lexer import tokenize


def test_parser_estrutura_basica_programa():
    codigo = "ohjelma loppu"
    tokens = list(tokenize(codigo))
    parser = Parser(tokens)

    ast = parser.parse_program()

    assert isinstance(ast, ProgramNode)
    assert len(ast.body) == 0


def test_parser_comando_kirjoita():
    codigo = 'ohjelma kirjoita("Hello, world"). loppu'
    tokens = list(tokenize(codigo))
    parser = Parser(tokens)

    ast = parser.parse_program()

    node_print = ast.body[0]

    assert (
        len(ast.body) == 1
    )  # Verifica se o parser coloca 1 comando dentro do corpo do programa
    assert isinstance(node_print, PrintNode)
    assert node_print.value == '"Hello, world"'


def test_parser_declaracao_variavel():
    codigo = "ohjelma kokonaisluku x, y. loppu"
    tokens = list(tokenize(codigo))
    parser = Parser(tokens)

    ast = parser.parse_program()

    node_decl = ast.body[0]

    assert isinstance(node_decl, VarDeclNode)
    assert node_decl.var_type == "TYPE_INT"
    assert node_decl.variables == ["x", "y"]
