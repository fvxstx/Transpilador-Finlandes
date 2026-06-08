from front.ast_nodes import (
    AssignNode,
    IfNode,
    PrintNode,
    ProgramNode,
    ReadNode,
    VarDeclNode,
    WhileNode,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def consume(self, expected_type=None):
        if self.pos >= len(self.tokens):
            return None
        token = self.tokens[self.pos]
        if expected_type and token.type != expected_type:
            return None
        self.pos += 1
        return token

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse_program(self):
        # self.consume("PROGRAM")
        # body = []

        # while self.peek() and self.peek().type != "ENDPROG":
        #     stmt = self.parse_statement()
        #     if stmt:
        #         body.append(stmt)

        # self.consume("ENDPROG")
        # return ProgramNode(body)

        if not self.peek() or self.peek().type != "PROGRAM":
            raise SyntaxError(
                "Erro de sintaxe: O programa deve começar com a palavra reservada 'ohjelma'."
            )
        self.consume("PROGRAM")

        body = []

        while self.peek() and self.peek().type != "ENDPROG":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        if not self.peek() or self.peek().type != "ENDPROG":
            raise SyntaxError(
                "Erro de sintaxe: O programa deve terminar com a palavra reservada 'loppu'."
            )
        self.consume("ENDPROG")

        return ProgramNode(body)

    def parse_statement(self):
        p = self.peek()
        if not p:
            return None

        t = p.type

        if t in ("TYPE_INT", "TYPE_DEC", "TYPE_STR", "TYPE_BOOL"):
            return self.parse_declaration()
        if t == "ID":
            return self.parse_assignment()
        if t == "READ":
            return self.parse_read()
        if t == "WHILE":
            return self.parse_while()
        if t == "WRITE":
            return self.parse_write()
        if t == "IF":
            return self.parse_if()

        self.pos += 1
        return None

    def parse_write(self):
        # self.consume("WRITE")
        # self.consume("LPAREN")
        # val = ""
        # while self.peek() and self.peek().type != "RPAREN":
        #     token = self.consume()
        #     val += token.value + " "
        # self.consume("RPAREN")
        # self.consume("DOT")

        # return PrintNode(value=val.strip())

        self.consume("WRITE")
        self.consume("LPAREN")
        val = ""

        while self.peek() and self.peek().type != "RPAREN":
            token = self.consume()
            val += token.value + " "
        self.consume("RPAREN")

        if not self.peek() or self.peek().type != "DOT":
            raise SyntaxError(
                "Erro de sintaxe: Esperado um ponto '.' no final do comando 'kirjoita'"
            )
        self.consume("DOT")

        return PrintNode(value=val.strip())

    def parse_if(self):
        self.consume("IF")
        self.consume("LPAREN")
        cond = ""
        while self.peek() and self.peek().type != "RPAREN":
            token = self.consume()
            cond += token.value + " "
        self.consume("RPAREN")
        self.consume("LBRACE")

        body = []
        while self.peek() and self.peek().type != "RBRACE":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        self.consume("RBRACE")

        else_body = None
        if self.peek() and self.peek().type == "ELSE":
            self.consume("ELSE")
            self.consume("LBRACE")
            else_body = []
            while self.peek() and self.peek().type != "RBRACE":
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
            self.consume("RBRACE")

        return IfNode(condition=cond.strip(), body=body, else_body=else_body)

    def parse_declaration(self):
        type_token = self.consume()
        ids = []

        while True:
            token_id = self.consume("ID")
            if not token_id:
                break
            ids.append(token_id.value)

            if not self.peek() or self.peek().type != "COMMA":
                break
            self.consume("COMMA")

        self.consume("DOT")
        return VarDeclNode(var_type=type_token.type, variables=ids)

    def parse_assignment(self):
        var_token = self.consume("ID")
        self.consume("ASSIGN")

        expr = ""
        while self.peek() and self.peek().type != "DOT":
            token = self.consume()
            expr += token.value + " "

        self.consume("DOT")
        return AssignNode(var_name=var_token.value, value=expr.strip())

    def parse_read(self):
        self.consume("READ")
        self.consume("LPAREN")
        var_token = self.consume("ID")
        self.consume("RPAREN")
        self.consume("DOT")

        name = var_token.value if var_token else ""
        return ReadNode(var_name=name)

    def parse_while(self):
        self.consume("WHILE")
        self.consume("LPAREN")

        cond = ""
        while self.peek() and self.peek().type != "RPAREN":
            token = self.consume()
            cond += token.value + " "

        self.consume("RPAREN")
        self.consume("LBRACE")

        body = []
        while self.peek() and self.peek().type != "RBRACE":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        self.consume("RBRACE")
        return WhileNode(condition=cond.strip(), body=body)
