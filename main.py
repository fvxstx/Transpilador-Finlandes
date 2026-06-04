import tkinter as tk

from interface import InterfaceApp


def main() -> None:
    root = tk.Tk()
    app = InterfaceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
