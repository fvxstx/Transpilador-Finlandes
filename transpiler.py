# --- TRANSPILER ---
class FinlandesTranspiler:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.indent_level = 0

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

    def get_indent(self):
        return "    " * self.indent_level

    def convert_expression_token(self, value):
        replacements = {
            "tosi": "True",
            "epätosi": "False"
        }
        return replacements.get(value, value)

    def parse_program(self):
        code = "def run_program():\n"
        self.indent_level = 1

        if not self.consume('PROGRAM'):
            return "# Use 'ohjelma' para começar"

        while self.peek() and self.peek().type != 'ENDPROG':
            stmt = self.parse_statement()
            if stmt:
                code += stmt

        self.consume('ENDPROG')
        code += "\nrun_program()"
        return code

    def parse_statement(self):
        p = self.peek()
        if not p:
            return ""

        t = p.type

        if t in ('TYPE_INT', 'TYPE_DEC', 'TYPE_STR', 'TYPE_BOOL'):
            return self.parse_declaration()
        if t == 'WRITE':
            return self.parse_write()
        if t == 'READ':
            return self.parse_read()
        if t == 'ID':
            return self.parse_assignment()
        if t == 'IF':
            return self.parse_if()
        if t == 'ELSE':
            return self.parse_else()
        if t == 'WHILE':
            return self.parse_while()

        self.pos += 1
        return ""

    def parse_declaration(self):
        type_token = self.consume()
        ids = []
        default_value = "0"

        if type_token.type == 'TYPE_DEC':
            default_value = "0.0"
        elif type_token.type == 'TYPE_STR':
            default_value = '""'
        elif type_token.type == 'TYPE_BOOL':
            default_value = "False"

        while True:
            token_id = self.consume('ID')
            if not token_id:
                break
            ids.append(f"{token_id.value} = {default_value}")
            if not self.peek() or self.peek().type != 'COMMA':
                break
            self.consume('COMMA')

        self.consume('DOT')
        return "\n".join([self.get_indent() + i for i in ids]) + "\n"

    def parse_read(self):
        self.consume('READ')
        self.consume('LPAREN')
        var_token = self.consume('ID')
        self.consume('RPAREN')
        self.consume('DOT')
        if var_token:
            return f"{self.get_indent()}{var_token.value} = terminal_input('{var_token.value}')\n"
        return ""

    def parse_assignment(self):
        var_token = self.consume('ID')
        self.consume('ASSIGN')
        expr = ""
        while self.peek() and self.peek().type != 'DOT':
            token = self.consume()
            expr += self.convert_expression_token(token.value) + " "
        self.consume('DOT')
        return f"{self.get_indent()}{var_token.value} = {expr.strip()}\n"

    def parse_write(self):
        self.consume('WRITE')
        self.consume('LPAREN')
        val = ""
        while self.peek() and self.peek().type != 'RPAREN':
            token = self.consume()
            val += self.convert_expression_token(token.value) + " "
        self.consume('RPAREN')
        self.consume('DOT')
        return f"{self.get_indent()}print({val.strip()})\n"

    def parse_if(self):
        self.consume('IF')
        self.consume('LPAREN')
        cond = ""
        while self.peek() and self.peek().type != 'RPAREN':
            token = self.consume()
            cond += self.convert_expression_token(token.value) + " "
        self.consume('RPAREN')
        self.consume('LBRACE')
        self.indent_level += 1
        body = ""
        while self.peek() and self.peek().type != 'RBRACE':
            body += self.parse_statement()
        self.indent_level -= 1
        self.consume('RBRACE')
        return f"{self.get_indent()}if {cond.strip()}:\n{body or self.get_indent()+'    pass'}\n"

    def parse_else(self):
        self.consume('ELSE')
        self.consume('LBRACE')
        self.indent_level += 1
        body = ""
        while self.peek() and self.peek().type != 'RBRACE':
            body += self.parse_statement()
        self.indent_level -= 1
        self.consume('RBRACE')
        return f"{self.get_indent()}else:\n{body or self.get_indent()+'    pass'}\n"

    def parse_while(self):
        self.consume('WHILE')
        self.consume('LPAREN')
        cond = ""
        while self.peek() and self.peek().type != 'RPAREN':
            token = self.consume()
            cond += self.convert_expression_token(token.value) + " "
        self.consume('RPAREN')
        self.consume('LBRACE')
        self.indent_level += 1
        body = ""
        while self.peek() and self.peek().type != 'RBRACE':
            body += self.parse_statement()
        self.indent_level -= 1
        self.consume('RBRACE')
        return f"{self.get_indent()}while {cond.strip()}:\n{body or self.get_indent()+'    pass'}\n"