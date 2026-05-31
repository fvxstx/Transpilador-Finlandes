from dataclasses import dataclass


class ASTNode:
    pass


@dataclass
class ProgramNode(ASTNode):
    body: list[ASTNode]


@dataclass
class VarDeclNode(ASTNode):
    var_type: str
    variables: list[str]


@dataclass
class AssignNode(ASTNode):
    var_name: str
    value: str


@dataclass
class PrintNode(ASTNode):
    value: str


@dataclass
class ReadNode(ASTNode):
    var_name: str


@dataclass
class IfNode(ASTNode):
    condition: str
    body: list[ASTNode]


@dataclass
class WhileNode(ASTNode):
    condition: str
    body: list[ASTNode]
