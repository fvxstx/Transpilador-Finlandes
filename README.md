# Transpilador Finlandês usando Python
- **Professor:** Eduardo Xavier
- **Curso:** Ciência da Computação
- **Matéria:** Teoria da Computação e Compiladores
- **Instituição:** UNIFACS — Universidade Salvador
- **Projeto:** Desenvolvimento de um Transpilador (Finlandês)
- **Linguagem Usada:** Python
  
## Download no Drive
[📥 Baixar Executável (.exe)](https://drive.google.com/file/d/1vUV6gdXXJC8DtWe6ccLXiB1CGAJzwND3/view?usp=sharing)

### Autores

| Nome | RA |
|------|----|
| Fausto Bento Torres | 1272521583 |
| Rafael Pereira Grigorio de Lacerda | 1272526033 |
| José Felipe Amorim Gerez | 12725158186 |
| Vinicius Lacerda Santos | 12725210686 |
| Yuri Cruz Torquato | 12724219602 |

---

# 1. Introdução

Este projeto consiste em um **transpilador na lingua finlandesa usando Python**, acompanhado de uma **IDE própria desenvolvida em Tkinter**.

O objetivo principal do projeto é demonstrar visualmente o funcionamento interno de um compilador/transpilador utilizando conceitos clássicos da área de compiladores:

- Análise Léxica (Lexer)
- Análise Sintática (Parser)
- Construção da AST (Árvore Sintática Abstrata)
- Geração de Código (Code Generation)
- Execução Dinâmica
- Interface de Desenvolvimento

Diferente de um compilador tradicional que gera código binário, este projeto realiza uma **transpilação**, convertendo código escrito em uma linguagem para outra linguagem de alto nível (Python).

Todo o processo ocorre em tempo real dentro da própria IDE.

---

# 2. Objetivo do Projeto

Este projeto foi desenvolvido como parte da atividade A3 da disciplina de Teoria da Computação e Compiladores, com o objetivo de aplicar na prática conceitos estudados durante o curso relacionados à construção de linguagens, análise léxica, análise sintática, árvores sintáticas abstratas (AST) e geração de código.

Para isso, foi criada uma linguagem simples e educativa utilizando palavras inspiradas no finlandês, permitindo que o usuário:

- Escreva programas usando comandos próprios.
- Veja instantaneamente o código convertido para Python.
- Execute diretamente dentro da interface.
- Entenda visualmente como linguagens de programação funcionam internamente.
- Compreenda o fluxo de tradução entre diferentes linguagens de programação.
- Observe na prática as etapas fundamentais utilizadas em compiladores e transpiladores.

---

# 3. Tecnologias Utilizadas

O projeto foi desenvolvido utilizando recursos nativos da linguagem Python, sem a necessidade de frameworks externos.

### Linguagem

- Python 3

### Bibliotecas Utilizadas

- Tkinter (Interface Gráfica)
- threading (Execução paralela)
- queue (Comunicação entre interface e execução)
- re (Expressões regulares)
- dataclasses (Estruturas de dados)

### Paradigmas e Conceitos Aplicados

- Programação Orientada a Objetos (POO)
- Expressões Regulares
- Estruturas de Dados
- Árvores Sintáticas Abstratas (AST)
- Análise Léxica
- Análise Sintática
- Geração de Código
- Transpilação

---

# 4. Como Executar o Projeto

## Pré-requisitos

- Python 3 instalado na máquina

## Execução

Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

Após a execução, a IDE será aberta automaticamente.

---

# 5. Exemplo Completo de Programa

Código escrito na linguagem finlandesa:

```finlandes
ohjelma

kokonaisluku idade.

kirjoita("Digite sua idade").
lue(idade).

jos (idade >= 18) {
    kirjoita("Maior de idade").
}

loppu
```

Código Python gerado:

```python
def run_program():
    idade = 0

    print("Digite sua idade")
    idade = terminal_input("idade")

    if idade >= 18:
        print("Maior de idade")

run_program()
```

---

# 6. Visão Geral da Arquitetura

O sistema foi dividido em módulos independentes.

```
Usuário
   ↓
Editor Finlandês
   ↓
Lexer (Tokenização)
   ↓
Parser
   ↓
AST
   ↓
Gerador Python
   ↓
Execução
   ↓
Terminal Integrado
```

---

# 7. Estrutura do Projeto

```plaintext
Projeto
│
├── Front/
│   ├── analisador.py
│   ├── ast_nodes.py
│   └── gerador.py
│
├── interface.py
├── lexer.py
├── config.py
└── main.py
```

---

# 8. Funcionamento Completo do Sistema

---

## 8.1 Lexer (Analisador Léxico)

Arquivo responsável por transformar texto em tokens.

Entrada:

```finlandes
idade := 18.
```

Saída:

```plaintext
ID("idade")
ASSIGN(":=")
NUMBER_INT("18")
DOT(".")
```

O lexer utiliza expressões regulares para identificar e classificar os elementos da linguagem em tokens.

Trecho principal:

```python
TOKEN_SPEC = [
 ('PROGRAM', r'ohjelma'),
 ('IF', r'jos'),
 ('WHILE', r'kunnes'),
 ('READ', r'lue'),
 ('WRITE', r'kirjoita')
]
```

Cada padrão possui:

| Campo | Função |
|--------|--------|
| Tipo | Categoria do token |
| Regex | Como localizar |

Exemplo:

```python
('IF', r'jos')
```

Significa:

Sempre que encontrar:

```finlandes
jos
```

gera:

```plaintext
IF
```

---

## 8.2 Tokenização

Função:

```python
tokenize()
```

Responsável por:

1. Ler texto
2. Encontrar padrões
3. Gerar objetos Token

Estrutura:

```python
@dataclass
class Token:
    type:str
    value:str
```

Exemplo:

Entrada:

```finlandes
kirjoita("Olá").
```

Resultado:

```plaintext
WRITE
LPAREN
STRING
RPAREN
DOT
```

---

# 9. Parser

Arquivo:

```plaintext
Front/analisador.py
```

Responsável por transformar tokens em uma árvore lógica.

Exemplo:

Código:

```finlandes
jos (idade > 18) {
    kirjoita("Maior")
}
```

AST:

```plaintext
IfNode
├── condição
└── bloco
```

Fluxo:

```plaintext
Tokens
 ↓
Parser
 ↓
AST
```

---

# 10. Funções principais

### consume()

Consome o token atual.

```python
consume(expected_type)
```

Exemplo:

```python
consume("IF")
```

Verifica:

```plaintext
Token atual = IF
```

e avança.

---

### peek()

Olha próximo token sem consumir.

```python
peek()
```

Usado para prever decisões.

---

### parse_program()

Lê programa inteiro.

Reconhece:

```finlandes
ohjelma
...
loppu
```

Transforma em:

```plaintext
ProgramNode
```

---

### parse_statement()

Decide qual comando executar.

Reconhece:

```plaintext
Declaração
Atribuição
IF
WHILE
PRINT
READ
```

---

### parse_if()

Transforma:

```finlandes
jos (idade > 18)
```

em:

```plaintext
IfNode
```

---

### parse_while()

Transforma:

```finlandes
kunnes (...)
```

em:

```plaintext
WhileNode
```

---

# 11. AST (Árvore Sintática Abstrata)

Representação estruturada do programa.

Arquivo:

```plaintext
ast_nodes.py
```

Classes:

```python
ProgramNode
VarDeclNode
AssignNode
PrintNode
ReadNode
IfNode
WhileNode
```

Exemplo:

Código:

```finlandes
x := 10.
```

AST:

```plaintext
AssignNode
├── variável = x
└── valor = 10
```

---

# 12. Gerador de Código Python

Arquivo:

```plaintext
gerador.py
```

Classe:

```python
PythonCodeGenerator
```

Função:

```python
generate()
```

Transforma:

```finlandes
kirjoita("Oi").
```

em:

```python
print("Oi")
```

---

## Conversão de expressões

Método:

```python
convert_expression()
```

Substitui:

```plaintext
tosi → True
epätosi → False
```

---

## Conversão de estruturas

### Declaração

Entrada:

```finlandes
kokonaisluku idade.
```

Saída:

```python
idade = 0
```

---

### Entrada

Entrada:

```finlandes
lue(nome).
```

Saída:

```python
nome = terminal_input("nome")
```

---

### Saída

Entrada:

```finlandes
kirjoita("Texto").
```

Saída:

```python
print("Texto")
```

---

# 13. Interface Gráfica (Tkinter)

Arquivo:

```plaintext
interface.py
```

A IDE foi desenvolvida utilizando Tkinter.

Interface dividida em 4 áreas.

---

## Área 1 — Dicionário

Exibe referência rápida.

Exemplo:

```plaintext
ohjelma → início
jos → if
kunnes → while
```

Objetivo:

Ajudar aprendizado da linguagem.

---

## Área 2 — Código Finlandês

Editor principal.

Responsável por:

- Digitação
- Atualização automática
- Geração instantânea

---

## Área 3 — Tradução Python

Exibe código Python gerado.

Atualização:

```python
update_translation()
```

Executado automaticamente.

---

## Área 4 — Terminal Real

Executa o código.

Possui:

- Entrada do usuário
- Impressão em tempo real
- Tratamento de tipos

Funções:

```python
terminal_input()
custom_print()
```

---

# 14. Sistema de Execução

Fluxo:

```plaintext
Executar
↓
Thread separada
↓
exec()
↓
Terminal
```

Execução:

```python
exec(py_code)
```

Thread:

```python
threading.Thread()
```

Evita congelamento da interface.

---

# 15. Conceitos de Compiladores Aplicados

| Conceito | Implementado |
|----------|-------------|
| Lexer | Sim |
| Parser | Sim |
| AST | Sim |
| Geração de código | Sim |
| Execução | Sim |
| Interface | Sim |
| Entrada dinâmica | Sim |
| Tradução em tempo real | Sim |

---

# 16. Diferenciais

- Linguagem própria baseada em finlandês
- IDE integrada
- Tradução instantânea
- Execução em tempo real
- Parser manual
- AST personalizada
- Arquitetura modular
- Interface desktop

---

# 17. Conclusão

Este projeto demonstra o fluxo completo de construção de uma linguagem de programação.

O usuário escreve em uma linguagem de alto nível baseada em finlandês, o sistema interpreta os tokens, gera uma árvore sintática, converte para Python e executa o resultado diretamente na interface.

Além de funcionar como ferramenta prática, esse projeto da A3 também serve como estudo de:

- Compiladores
- Linguagens formais
- Parsing
- Estruturas de dados
- Interfaces gráficas
- Geração de código
- Arquitetura de software

```
Escrever → Tokenizar → Interpretar → Gerar → Executar
```

---
