import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

# --- FASE 1: ANALISADOR LÉXICO (LEXER) ---
TOKEN_SPEC = [
    ('PROGRAM',    r'ohjelma'),          
    ('ENDPROG',    r'loppu'),            
    ('TYPE_INT',   r'kokonaisluku'),     
    ('TYPE_DEC',   r'desimaali'),        
    ('TYPE_STR',   r'merkkijono'),       
    ('TYPE_BOOL',  r'totuusarvo'),       
    ('IF',         r'jos'),              
    ('ELSE',       r'muuten'),           
    ('DO',         r'tee'),              
    ('WHILE',      r'kunnes'),           
    ('READ',       r'lue'),              
    ('WRITE',      r'kirjoita'),         
    ('NUMBER_DEC', r'\d+\.\d+'),         
    ('NUMBER_INT', r'\d+'),              
    ('STRING',     r'"[^"]*"'),          
    ('ID',         r'[a-zA-Z_]\w*'),     
    ('ASSIGN',     r':='),               
    ('OP_REL',     r'[<>!=]=|[<>]|=='),  
    ('PLUS',       r'\+'),               
    ('MINUS',      r'-'),                
    ('MUL',        r'\*'),               
    ('DIV',        r'/'),                
    ('LPAREN',     r'\('),               
    ('RPAREN',     r'\)'),               
    ('LBRACE',     r'\{'),               
    ('RBRACE',     r'\}'),               
    ('COMMA',      r','),                
    ('DOT',        r'\.'),               
    ('WS',         r'\s+'),
    ('COMMENT',    r'#.*'), # Suporte a comentários para não dar erro léxico
]

regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

def tokenize(text):
    line, col, pos = 1, 1, 0
    while pos < len(text):
        match = re.match(regex, text[pos:])
        if not match: raise SyntaxError(f"Erro Léxico: '{text[pos]}' em {line}:{col}")
        kind, value = match.lastgroup, match.group()
        if kind not in ('WS', 'COMMENT'): 
            yield Token(kind, value, line, col)
        if '\n' in value:
            line += value.count('\n')
            col = len(value) - value.rfind('\n')
        else: col += len(value)
        pos += len(value)

# --- FASE 2: ANALISADOR SINTÁTICO E SEMÂNTICO (PARSER) ---
class FinlandesTranspiler:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.indent_level = 0
        # TABELA DE SÍMBOLOS: Armazena {'nome_da_var': 'TIPO'} 
        self.symbol_table = {} 

    def consume(self, expected_type=None):
        if self.pos >= len(self.tokens):
            raise Exception("Erro: Fim de arquivo inesperado.")
        token = self.tokens[self.pos]
        if expected_type and token.type != expected_type:
            raise Exception(f"Linha {token.line}: Esperado {expected_type}, mas encontrou {token.type} ('{token.value}')")
        self.pos += 1
        return token

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def get_indent(self):
        return "    " * self.indent_level

    def parse_program(self):
        code = ""
        self.consume('PROGRAM')
        while self.peek() and self.peek().type != 'ENDPROG':
            code += self.parse_statement()
        self.consume('ENDPROG')
        return code

    def parse_statement(self):
        t = self.peek().type
        if t in ('TYPE_INT', 'TYPE_DEC', 'TYPE_STR', 'TYPE_BOOL'):
            return self.parse_declaration()
        elif t == 'WRITE': return self.parse_write()
        elif t == 'ID': return self.parse_assignment()
        elif t == 'IF': return self.parse_if()
        elif t == 'DO': return self.parse_do_while()
        else:
            self.pos += 1
            return ""

    def parse_declaration(self):
        # Mapeia o token de tipo para uma categoria interna [cite: 18]
        type_token = self.consume()
        var_type = type_token.type 
        
        ids = []
        while True:
            token_id = self.consume('ID')
            # Guarda na tabela de símbolos para verificação posterior [cite: 29]
            self.symbol_table[token_id.value] = var_type
            ids.append(f"{token_id.value} = None")
            if self.peek().type != 'COMMA': break
            self.consume('COMMA')
        self.consume('DOT')
        return "\n".join([self.get_indent() + i for i in ids]) + "\n"

    def parse_assignment(self):
        var_token = self.consume('ID')
        var_name = var_token.value
        
        # VERIFICAÇÃO 1: Variável declarada? [cite: 29]
        if var_name not in self.symbol_table:
            raise Exception(f"Erro Semântico: Variável '{var_name}' não foi declarada.")
        
        target_type = self.symbol_table[var_name]
        self.consume('ASSIGN')
        
        # Processa a expressão e verifica tipos [cite: 26]
        expr_code, expr_type = self.parse_expression()
        
        # VERIFICAÇÃO 2: Compatibilidade de tipos (Simplificada) [cite: 26]
        if target_type == 'TYPE_INT' and expr_type == 'TYPE_STR':
            raise Exception(f"Erro Semântico na linha {var_token.line}: Não é possível atribuir uma STRING à variável inteira '{var_name}'.")
        
        self.consume('DOT')
        return f"{self.get_indent()}{var_name} = {expr_code}\n"

    def parse_expression(self):
        # Implementação básica para testar: ID + ID ou ID + constante
        left_token = self.consume()
        left_val = left_token.value
        
        # Tenta descobrir o tipo do operando esquerdo
        if left_token.type == 'ID':
            left_type = self.symbol_table.get(left_val, 'UNKNOWN')
        elif left_token.type == 'STRING': left_type = 'TYPE_STR'
        else: left_type = 'TYPE_INT'

        # Se houver um operador de soma
        if self.peek() and self.peek().type == 'PLUS':
            self.consume('PLUS')
            right_code, right_type = self.parse_expression()
            
            # VERIFICAÇÃO DE SOMA INVÁLIDA [cite: 26]
            if (left_type == 'TYPE_STR' and right_type != 'TYPE_STR') or \
               (left_type != 'TYPE_STR' and right_type == 'TYPE_STR'):
                raise Exception(f"Erro Semântico: Operação inválida entre {left_type} e {right_type}.")
            
            return f"{left_val} + {right_code}", left_type
        
        return left_val, left_type

    def parse_write(self):
        self.consume('WRITE')
        self.consume('LPAREN')
        val = self.consume().value
        self.consume('RPAREN')
        self.consume('DOT')
        return f"{self.get_indent()}print({val})\n"

    def parse_if(self):
        self.consume('IF')
        self.consume('LPAREN')
        # Simplificado para fins de teste
        cond = f"{self.consume().value} {self.consume('OP_REL').value} {self.consume().value}"
        self.consume('RPAREN')
        self.consume('LBRACE')
        self.indent_level += 1
        body = ""
        while self.peek().type != 'RBRACE':
            body += self.parse_statement()
        self.indent_level -= 1
        self.consume('RBRACE')
        return f"{self.get_indent()}if {cond}:\n{body}"

    def parse_do_while(self):
        self.consume('DO')
        self.consume('LBRACE')
        self.indent_level += 1
        body = ""
        while self.peek().type != 'RBRACE':
            body += self.parse_statement()
        self.indent_level -= 1
        self.consume('RBRACE')
        self.consume('WHILE')
        self.consume('LPAREN')
        cond = f"{self.consume().value} {self.consume('OP_REL').value} {self.consume().value}"
        self.consume('RPAREN')
        self.consume('DOT')
        return f"{self.get_indent()}while True:\n{body}{self.get_indent()}    if not ({cond}): break\n"

# --- ÁREA DE TESTE ---
source_error = """
ohjelma
    kokonaisluku a.
    # Esqueci o parentese: jos a > 10 {
    jos a > 10 {
        kirjoita("Erro aqui").
    }
loppu
"""

try:
    tokens = tokenize(source_error)
    transpiler = FinlandesTranspiler(tokens)
    python_code = transpiler.parse_program()
    
    with open("resultado.py", "w") as f:
        f.write(python_code)
    print("Sucesso! Arquivo gerado.")
except Exception as e:
    print(f"TESTE DE ERRO CAPTURADO: {e}")