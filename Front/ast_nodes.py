from dataclasses import dataclass
from typing import List, Any

class ASTNode:
    pass

@dataclass
class ProgramNode(ASTNode):
    body: List[ASTNode]

@dataclass
class VarDeclNode(ASTNode):
    var_type: str
    variables: List[str]

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
    body: List[ASTNode]

@dataclass
class WhileNode(ASTNode):
    condition: str
    body: List[ASTNode]