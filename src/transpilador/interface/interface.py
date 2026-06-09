import threading
import tkinter as tk
from queue import Queue
from tkinter import scrolledtext
from typing import Any, Dict

from src.transpilador.codegen.gerador import PythonCodeGenerator
from src.transpilador.config import DICTIONARY
from src.transpilador.lexer.lexer import tokenize
from src.transpilador.parser.analisador import Parser


class InterfaceApp:
    OUTPUT_POLL_INTERVAL = 100
    TERMINAL_PROMPT = "{} > "

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Finlandês IDE - Professional Edition")

        try:
            self.root.state("zoomed")
        except:
            pass

        self.colors: Dict[str, str] = {
            "bg": "#121212",
            "sidebar": "#1e1e1e",
            "text": "#e0e0e0",
            "accent": "#00aaff",
            "term_bg": "#0a0a0a",
            "green": "#4caf50",
        }

        self.fonts: Dict[str, Any] = {
            "title": ("Segoe UI", 9, "bold"),
            "editor": ("Consolas", 11),
            "button": ("Segoe UI", 10, "bold"),
        }

        self.input_queue = Queue()
        self.output_queue = Queue()
        self.is_running = False
        self.prompt_index = "1.0"
        self.widgets: Dict[str, scrolledtext.ScrolledText] = {}

        self.setup_ui()
        self.load_dictionary()
        self.load_calculator_example()

    def setup_ui(self) -> None:
        self.root.configure(bg=self.colors["bg"])

        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = [
            ("Dicionário", "dict"),
            ("Código Finlandês", "in"),
            ("Tradução Python", "out"),
            ("Terminal Real", "term"),
        ]

        for index, (label_text, key) in enumerate(columns):
            column_frame = tk.Frame(main_frame, bg=self.colors["bg"])
            column_frame.grid(row=0, column=index, sticky="nsew", padx=2)

            main_frame.grid_columnconfigure(index, weight=1)
            main_frame.grid_rowconfigure(0, weight=1)

            tk.Label(
                column_frame,
                text=label_text.upper(),
                font=self.fonts["title"],
                bg=self.colors["bg"],
                fg=self.colors["accent"],
            ).pack(pady=2)

            background = self.colors["term_bg"] if key == "term" else "#1e1e1e"
            foreground = "#00ff00" if key == "term" else self.colors["text"]

            widget = scrolledtext.ScrolledText(
                column_frame,
                font=self.fonts["editor"],
                bg=background,
                fg=foreground,
                insertbackground="white",
                bd=0,
            )
            widget.pack(fill=tk.BOTH, expand=True)
            self.widgets[key] = widget

        self.widgets["in"].bind("<KeyRelease>", self.update_translation)
        self.widgets["term"].bind("<Return>", self.handle_terminal_enter)
        self.widgets["term"].bind("<BackSpace>", self.handle_backspace)

        button_frame = tk.Frame(self.root, bg=self.colors["bg"])
        button_frame.pack(fill=tk.X)

        self.run_btn = tk.Button(
            button_frame,
            text="EXECUTAR PROGRAMA (RUN)",
            command=self.start_execution_thread,
            bg=self.colors["green"],
            fg="white",
            font=self.fonts["button"],
            relief=tk.FLAT,
            padx=20,
            pady=8,
        )
        self.run_btn.pack(pady=10)

        self.set_widget_state("dict", tk.DISABLED)
        self.set_widget_state("out", tk.DISABLED)

    def set_widget_state(self, key: str, state: str) -> None:
        self.widgets[key].config(state=state)

    def append_terminal_output(self, message: str, prompt: bool = False) -> None:
        self.output_queue.put((message, prompt))

    def process_terminal_output(self) -> None:
        terminal = self.widgets["term"]
        while not self.output_queue.empty():
            message, is_prompt = self.output_queue.get()
            terminal.config(state=tk.NORMAL)
            terminal.insert(tk.END, message)
            if is_prompt:
                self.prompt_index = terminal.index(tk.END)
            terminal.see(tk.END)

        if self.is_running or not self.output_queue.empty():
            self.root.after(self.OUTPUT_POLL_INTERVAL, self.process_terminal_output)

    def handle_backspace(self, event: tk.Event) -> str:
        if self.widgets["term"].compare("insert", "<=", self.prompt_index):
            return "break"
        return ""

    def handle_terminal_enter(self, event: tk.Event) -> str:
        if not self.is_running:
            return "break"

        line_start = self.widgets["term"].index("insert linestart")
        current_line = self.widgets["term"].get(line_start, tk.END).strip()

        if ">" in current_line:
            user_input = current_line.split(">", 1)[-1].strip()
        else:
            user_input = current_line

        self.widgets["term"].insert(tk.END, "\n")
        self.widgets["term"].see(tk.END)
        self.input_queue.put(user_input)
        return "break"

    def load_dictionary(self) -> None:
        dictionary_text = "REFERÊNCIA DE SINTAXE\n" + "━" * 25 + "\n\n"
        for category, items in DICTIONARY.items():
            dictionary_text += f"[{category}]\n"
            for token, description in items.items():
                dictionary_text += f"{token.ljust(15)} : {description}\n"
            dictionary_text += "\n"

        self.set_widget_state("dict", tk.NORMAL)
        self.widgets["dict"].delete("1.0", tk.END)
        self.widgets["dict"].insert("1.0", dictionary_text)
        self.set_widget_state("dict", tk.DISABLED)

    def load_calculator_example(self) -> None:
        example_code = (
            "ohjelma\n"
            "  kokonaisluku opção, n1, n2, res.\n"
            "  opção := 0.\n"
            "  kunnes (opção != 9) {\n"
            '    kirjoita("--- CALCULADORA ---").\n'
            '    kirjoita("1:Soma | 2:Sub | 3:Mult | 4:Div | 9:Sair").\n'
            '    kirjoita("Escolha:").\n'
            "    lue(opção).\n\n"
            '    jos (opção == 9) { kirjoita("Adeus!"). }\n\n'
            "    jos (opção < 5) {\n"
            '      kirjoita("Numero 1:"). lue(n1).\n'
            '      kirjoita("Numero 2:"). lue(n2).\n\n'
            "      jos (opção == 1) { res := n1 + n2. }\n"
            "      jos (opção == 2) { res := n1 - n2. }\n"
            "      jos (opção == 3) { res := n1 * n2. }\n"
            "      jos (opção == 4) { res := n1 / n2. }\n"
            '      kirjoita("Resultado:").\n'
            "      kirjoita(res).\n"
            "    }\n"
            "  }\n"
            "loppu"
        )

        self.widgets["in"].delete("1.0", tk.END)
        self.widgets["in"].insert("1.0", example_code)
        self.update_translation()

    def update_translation(self, event: tk.Event | None = None) -> None:
        try:
            raw_text = self.widgets["in"].get("1.0", tk.END)
            tokens = tokenize(raw_text)
            ast_tree = Parser(tokens).parse_program()
            generated_code = PythonCodeGenerator().generate(ast_tree)
        except Exception as error:
            generated_code = f"# Erro de tradução:\n# {error}\n"

        self.set_widget_state("out", tk.NORMAL)
        self.widgets["out"].delete("1.0", tk.END)
        self.widgets["out"].insert("1.0", generated_code)
        self.set_widget_state("out", tk.DISABLED)

    def start_execution_thread(self) -> None:
        if self.is_running:
            return

        self.input_queue = Queue()
        self.output_queue = Queue()
        self.widgets["term"].config(state=tk.NORMAL)
        self.widgets["term"].delete("1.0", tk.END)
        self.widgets["term"].insert(tk.END, "--- INICIANDO EXECUÇÃO ---\n")
        self.widgets["term"].see(tk.END)

        self.is_running = True
        self.run_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.execute_code, daemon=True).start()
        self.root.after(self.OUTPUT_POLL_INTERVAL, self.process_terminal_output)

    def execute_code(self) -> None:
        python_code = self.widgets["out"].get("1.0", tk.END)

        def terminal_input(var_name: str):
            self.append_terminal_output(f"{var_name} > ", prompt=True)
            val = self.input_queue.get().strip()
            val_lower = val.lower()

            if val_lower in ("tosi", "true"):
                return True
            if val_lower in ("epätosi", "false"):
                return False

            try:
                if "." in val:
                    return float(val)
                return int(val)
            except Exception:
                return val

        def custom_print(*args: Any) -> None:
            message = " ".join(map(str, args)) + "\n"
            self.append_terminal_output(message)

        try:
            exec(python_code, {
                "terminal_input": terminal_input,
                "print": custom_print,
            })
        except Exception as e:
            custom_print(f"\nERRO DE EXECUÇÃO: {e}")
        finally:
            self.is_running = False
            self.run_btn.config(state=tk.NORMAL)
            custom_print("\n--- PROGRAMA FINALIZADO ---")
