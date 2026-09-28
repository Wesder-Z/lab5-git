"""Точка запуска графического приложения."""

import tkinter as tk

from gui import Lab5Application


def main() -> None:
    """Создаёт главное окно и запускает цикл обработки событий."""
    root = tk.Tk()
    Lab5Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
