# Transpilador Finlandês - A3 Prof. Xavier

## 1. Autores

| Nome | RA |
|------|----|
| Fausto Bento Torres | 1272521583 |
| Rafael Pereira Grigorio de Lacerda | 1272526033 |
| José Felipe Amorim Gerez | 12725158186 |
| Vinicius | 000000 |
| Yuri Cruz Torquato | 12724219602 |

---

## 2. Sobre o projeto

Este projeto consiste em um **transpilador em Finlandês** que traduz uma linguagem fictícia baseada no finlandês para **Python**.

A ideia principal é permitir que o usuário escreva códigos em uma linguagem mais didática (com comandos como `ohjelma`, `kirjoita`, `jos`) e veja automaticamente a tradução e execução em Python.

O sistema também conta com uma **interface gráfica interativa**, facilitando testes e aprendizado.

---

## 3. Sobre o código

O projeto foi desenvolvido em Python e dividido em algumas partes principais:

### 🔹 Tokenização
- Usa **expressões regulares (`re`)** para quebrar o código em tokens.
- Cada token possui:
  - tipo (ex: `IF`, `NUMBER`)
  - valor (ex: `jos`, `42`)

### 🔹 Transpilador
- Classe `FinlandesTranspiler`
- Converte os tokens em código Python equivalente
- Suporte para:
  - variáveis
  - entrada (`lue`)
  - saída (`kirjoita`)
  - condições (`jos`)
  - loops (`kunnes`)

### 🔹 Interface gráfica
- Feita com **Tkinter**
- Dividida em 4 áreas:
  1. Dicionário da linguagem
  2. Código em finlandês
  3. Tradução para Python
  4. Terminal de execução

### 🔹 Execução
- O código traduzido é executado com `exec()`
- Entrada do usuário é tratada com fila (`Queue`)
- Execução ocorre em **thread separada**

---

## Estrutura visual da interface

| Área | Função |
|------|--------|
| Dicionário | Mostra comandos da linguagem |
| Código | Onde o usuário escreve |
| Tradução | Código Python gerado |
| Terminal | Execução em tempo real |

---

## 💡 4. Exemplos de códigos interativos

### 4.1 Jogo de adivinhação

```
ohjelma
  kokonaisluku segredo, palpite, tentativas.
  segredo := 76.
  palpite := 0.
  tentativas := 0.

  kirjoita("--- BEM-VINDO AO JOGO DE ADIVINHACAO ---").
  kirjoita("Tente descobrir o numero secreto entre 1 e 100.").

  kunnes (palpite != segredo) {
    kirjoita("Qual o seu palpite?").
    lue(palpite).
    
    tentativas := tentativas + 1.

    jos (palpite < segredo) {
      kirjoita("DICA: O numero e MAIOR!").
    }
    
    jos (palpite > segredo) {
      kirjoita("DICA: O numero e MENOR!").
    }
  }

  kirjoita("PARABENS! Voce acertou!").
  kirjoita("Total de tentativas:").
  kirjoita(tentativas).
loppu
```

### 4.2 Gerador de Tabuada

```
ohjelma
  kokonaisluku num, cont, res.
  cont := 1.
  kirjoita("Tabuada de qual numero?").
  lue(num).
  kunnes (cont != 11) {
    res := num * cont.
    kirjoita(res).
    cont := cont + 1.
  }
loppu
```

### 4.3 Cálculo de Fatorial

```
ohjelma
  kokonaisluku n, f.
  kirjoita("Digitem um numero:").
  lue(n).
  f := 1.
  kunnes (n > 1) {
    f := f * n.
    n := n - 1.
  }
  kirjoita("Fatorial:").
  kirjoita(f).
loppu
```

### 4.4 Verificador de Maioridade

```
ohjelma
  kokonaisluku idade.
  kirjoita("Sua idade:").
  lue(idade).
  jos (idade >= 18) {
    kirjoita("Maior de idade").
  }
  muuten {
    kirjoita("Menor de idade").
  }
loppu
```


// Melhorar esse README explicando melhor o codigo + Melhorar os exemplos de testes
// Esse será o nossa documentação