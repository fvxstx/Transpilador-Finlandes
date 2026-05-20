import threading
import tkinter as tk
from tkinter import scrolledtext
from queue import Queue

from Front.analisador import Parser
from Front.gerador import PythonCodeGenerator
from config import DICTIONARY
from lexer import tokenize

# --- INTERFACE APP ---
class InterfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finlandês IDE - Professional Edition")

        try:
            self.root.state('zoomed')
        except:
            pass

        self.colors = {
            "bg": "#121212",
            "sidebar": "#1e1e1e",
            "text": "#e0e0e0",
            "accent": "#00aaff",
            "term_bg": "#0a0a0a",
            "green": "#4caf50"
        }

        self.input_queue = Queue()
        self.is_running = False
        self.prompt_index = "1.0"

        self.setup_ui()
        self.load_dictionary()
        self.load_calculator_example()

    def setup_ui(self):
        self.root.configure(bg=self.colors["bg"])

        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = [
            ("Dicionário", "dict"),
            ("Código Finlandês", "in"),
            ("Tradução Python", "out"),
            ("Terminal Real", "term")
        ]

        self.widgets = {}

        for i, (title, key) in enumerate(cols):
            f = tk.Frame(main_frame, bg=self.colors["bg"])
            f.grid(row=0, column=i, sticky="nsew", padx=2)

            main_frame.grid_columnconfigure(i, weight=1)
            main_frame.grid_rowconfigure(0, weight=1)

            tk.Label(
                f,
                text=title.upper(),
                font=("Segoe UI", 9, "bold"),
                bg=self.colors["bg"],
                fg=self.colors["accent"]
            ).pack(pady=2)

            bg_color = self.colors["term_bg"] if key == "term" else "#1e1e1e"
            fg_color = "#00ff00" if key == "term" else self.colors["text"]

            txt = scrolledtext.ScrolledText(
                f,
                font=("Consolas", 11),
                bg=bg_color,
                fg=fg_color,
                insertbackground="white",
                bd=0
            )

            txt.pack(fill=tk.BOTH, expand=True)
            self.widgets[key] = txt

        self.widgets["in"].bind("<KeyRelease>", self.update_translation)
        self.widgets["term"].bind("<Return>", self.handle_terminal_enter)
        self.widgets["term"].bind("<BackSpace>", self.handle_backspace)

        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(fill=tk.X)

        self.run_btn = tk.Button(
            btn_frame,
            text="EXECUTAR PROGRAMA (RUN)",
            command=self.start_execution_thread,
            bg=self.colors["green"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        self.run_btn.pack(pady=10)

    def handle_backspace(self, event):
        if self.widgets["term"].compare("insert", "<=", self.prompt_index):
            return "break"

    def handle_terminal_enter(self, event):
        if not self.is_running:
            return "break"

        input_data = self.widgets["term"].get(self.prompt_index, tk.END).strip()
        self.widgets["term"].insert(tk.END, "\n")
        self.input_queue.put(input_data)
        self.widgets["term"].see(tk.END)
        return "break"

    def load_dictionary(self):
        text = "REFERÊNCIA DE SINTAXE\n" + "━" * 25 + "\n\n"
        for cat, items in DICTIONARY.items():
            text += f"[{cat}]\n"
            for k, v in items.items():
                text += f"{k.ljust(15)} : {v}\n"
            text += "\n"

        self.widgets["dict"].config(state=tk.NORMAL)
        self.widgets["dict"].insert("1.0", text)
        self.widgets["dict"].config(state=tk.DISABLED)

    def load_calculator_example(self):
        code = (
            'ohjelma\n'
            '  kokonaisluku opção, n1, n2, res.\n'
            '  opção := 0.\n'
            '  kunnes (opção != 9) {\n'
            '    kirjoita("--- CALCULADORA ---").\n'
            '    kirjoita("1:Soma | 2:Sub | 3:Mult | 4:Div | 9:Sair").\n'
            '    kirjoita("Escolha:").\n'
            '    lue(opção).\n\n'
            '    jos (opção == 9) { kirjoita("Adeus!"). }\n\n'
            '    jos (opção < 5) {\n'
            '      kirjoita("Numero 1:"). lue(n1).\n'
            '      kirjoita("Numero 2:"). lue(n2).\n\n'
            '      jos (opção == 1) { res := n1 + n2. }\n'
            '      jos (opção == 2) { res := n1 - n2. }\n'
            '      jos (opção == 3) { res := n1 * n2. }\n'
            '      jos (opção == 4) { res := n1 / n2. }\n'
            '      kirjoita("Resultado:").\n'
            '      kirjoita(res).\n'
            '    }\n'
            '  }\n'
            'loppu'
        )
        self.widgets["in"].insert("1.0", code)
        self.update_translation()

    def update_translation(self, event=None):
        try:
            raw_text = self.widgets["in"].get("1.0", tk.END)
            tokens = tokenize(raw_text)
            
            ast_tree = Parser(tokens).parse_program()
            py_code = PythonCodeGenerator().generate(ast_tree)

            self.widgets["out"].config(state=tk.NORMAL)
            self.widgets["out"].delete("1.0", tk.END)
            self.widgets["out"].insert("1.0", py_code)
            self.widgets["out"].config(state=tk.DISABLED)
        except Exception:
            pass

    def start_execution_thread(self):
        if self.is_running:
            return
        self.widgets["term"].delete("1.0", tk.END)
        self.widgets["term"].insert(tk.END, "--- INICIANDO EXECUÇÃO ---\n")
        self.is_running = True
        threading.Thread(target=self.execute_code, daemon=True).start()

    def execute_code(self):
        py_code = self.widgets["out"].get("1.0", tk.END)

        def terminal_input(var_name):
            self.widgets["term"].insert(tk.END, f"{var_name} > ")
            self.widgets["term"].see(tk.END)
            self.prompt_index = self.widgets["term"].index("insert")
            val = self.input_queue.get()
            val_lower = val.lower()

            if val_lower in ("tosi", "true"): return True
            if val_lower in ("epätosi", "false"): return False

            try:
                if '.' in val: return float(val)
                return int(val)
            except:
                return val

        def custom_print(*args):
            msg = " ".join(map(str, args)) + "\n"
            self.widgets["term"].insert(tk.END, msg)
            self.widgets["term"].see(tk.END)

        try:
            exec(py_code, {
                "terminal_input": terminal_input,
                "print": custom_print
            })
        except Exception as e:
            custom_print(f"\nERRO DE EXECUÇÃO: {e}")
        finally:
            self.is_running = False
            custom_print("\n--- PROGRAMA FINALIZADO ---")