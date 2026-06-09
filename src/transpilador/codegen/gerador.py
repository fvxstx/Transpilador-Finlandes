from src.transpilador.parser.ast_nodes import (
    AssignNode,
    ASTNode,
    IfNode,
    PrintNode,
    ProgramNode,
    ReadNode,
    VarDeclNode,
    WhileNode,
)


class PythonCodeGenerator:
    def __init__(self):
        self.indent_level = 1

    def get_indent(self):
        return "    " * self.indent_level

    def convert_expression(self, val):
        replacements = {"tosi": "True", "epätosi": "False"}
        for fin, py in replacements.items():
            val = val.replace(fin, py)
        return val

    def generate(self, node: ASTNode) -> str:
        if isinstance(node, ProgramNode):
            code = "def run_program():\n"
            for stmt in node.body:
                code += self.generate(stmt)
            code += "\nrun_program()"
            return code

        elif isinstance(node, PrintNode):
            val = self.convert_expression(node.value)
            return f"{self.get_indent()}print({val})\n"

        elif isinstance(node, IfNode):
            cond = self.convert_expression(node.condition)
            code = f"{self.get_indent()}if {cond}:\n"
            self.indent_level += 1

            if not node.body:
                code += f"{self.get_indent()}pass\n"
            else:
                for stmt in node.body:
                    code += self.generate(stmt)

            self.indent_level -= 1
            return code

        elif isinstance(node, VarDeclNode):
            default_value = "0"
            if node.var_type == "TYPE_DEC":
                default_value = "0.0"
            elif node.var_type == "TYPE_STR":
                default_value = '""'
            elif node.var_type == "TYPE_BOOL":
                default_value = "False"

            code = ""
            for var in node.variables:
                code += f"{self.get_indent()}{var} = {default_value}\n"
            return code

        elif isinstance(node, AssignNode):
            val = self.convert_expression(node.value)
            return f"{self.get_indent()}{node.var_name} = {val}\n"

        elif isinstance(node, ReadNode):
            return f"{self.get_indent()}{node.var_name} = terminal_input('{node.var_name}')\n"

        elif isinstance(node, WhileNode):
            cond = self.convert_expression(node.condition)
            code = f"{self.get_indent()}while {cond}:\n"

            self.indent_level += 1
            if not node.body:
                code += f"{self.get_indent()}pass\n"
            else:
                for stmt in node.body:
                    code += self.generate(stmt)
            self.indent_level -= 1

            return code

        return ""
