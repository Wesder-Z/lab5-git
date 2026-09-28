"""Графический интерфейс лабораторной работы № 5."""

import tkinter as tk
from tkinter import ttk

from currency import RATES_TO_RUB, convert_currency, format_amount


PADDING = 12


class GreetingTab(ttk.Frame):
    """Вкладка с кнопкой приветствия."""

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=PADDING)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Button(
            self,
            text="Привет",
            command=self.show_greeting,
        ).grid(row=0, column=0, pady=(0, PADDING))

        self.message = tk.StringVar(value="Нажмите кнопку")
        ttk.Label(
            self,
            textvariable=self.message,
            anchor="center",
            font=("TkDefaultFont", 14),
        ).grid(row=1, column=0, sticky="nsew")

    def show_greeting(self) -> None:
        """Показывает приветствие после нажатия кнопки."""
        self.message.set("Привет, Анатолий!")


class ConverterTab(ttk.Frame):
    """Вкладка конвертера валют с фиксированным учебным курсом."""

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=PADDING)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Сумма:").grid(
            row=0,
            column=0,
            sticky="w",
            pady=4,
        )
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=0, column=1, sticky="ew", pady=4)
        self.amount_entry.insert(0, "100")

        currencies = tuple(RATES_TO_RUB)
        ttk.Label(self, text="Из валюты:").grid(
            row=1,
            column=0,
            sticky="w",
            pady=4,
        )
        self.source_currency = tk.StringVar(value="USD")
        ttk.Combobox(
            self,
            textvariable=self.source_currency,
            values=currencies,
            state="readonly",
        ).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="В валюту:").grid(
            row=2,
            column=0,
            sticky="w",
            pady=4,
        )
        self.target_currency = tk.StringVar(value="RUB")
        ttk.Combobox(
            self,
            textvariable=self.target_currency,
            values=currencies,
            state="readonly",
        ).grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Button(
            self,
            text="Конвертировать",
            command=self.convert,
        ).grid(row=3, column=0, columnspan=2, pady=(PADDING, 4))

        self.result = tk.StringVar(value="Введите сумму и выберите валюты")
        self.result_label = ttk.Label(
            self,
            textvariable=self.result,
            anchor="center",
            wraplength=420,
        )
        self.result_label.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=4,
        )

    def convert(self) -> None:
        """Проверяет ввод и показывает результат конвертации."""
        try:
            converted = convert_currency(
                self.amount_entry.get(),
                self.source_currency.get(),
                self.target_currency.get(),
            )
        except (TypeError, ValueError) as error:
            self.result.set(f"Ошибка: {error}")
            return

        self.result.set(
            f"Результат: {format_amount(converted)} "
            f"{self.target_currency.get()}"
        )


class InfoWindow(tk.Toplevel):
    """Дополнительное интерактивное окно приложения."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.title("О лабораторной работе")
        self.geometry("380x190")
        self.minsize(340, 170)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        content = ttk.Frame(self, padding=PADDING)
        content.grid(sticky="nsew")
        content.columnconfigure(0, weight=1)

        self.details = tk.StringVar(
            value="Это отдельное окно. Нажмите кнопку для подробностей."
        )
        ttk.Label(
            content,
            textvariable=self.details,
            anchor="center",
            justify="center",
            wraplength=330,
        ).grid(row=0, column=0, sticky="ew", pady=(0, PADDING))

        ttk.Button(
            content,
            text="Показать автора",
            command=self.show_author,
        ).grid(row=1, column=0, pady=4)
        ttk.Button(
            content,
            text="Закрыть",
            command=self.destroy,
        ).grid(row=2, column=0, pady=4)

    def show_author(self) -> None:
        """Показывает сведения об авторе в дополнительном окне."""
        self.details.set("Борисов Анатолий Олегович, группа 221141")


class Lab5Application:
    """Главное окно, объединяющее задания варианта 5."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Лабораторная работа № 5")
        self.root.geometry("560x360")
        self.root.minsize(500, 320)
        self.root.resizable(True, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._create_menu()
        self._create_notebook()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)

    def _create_menu(self) -> None:
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Exit", command=self.exit_application)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def _create_notebook(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.grid(row=0, column=0, sticky="nsew", padx=PADDING, pady=PADDING)

        notebook.add(GreetingTab(notebook), text="Приветствие")
        notebook.add(ConverterTab(notebook), text="Конвертер валют")

        windows_tab = ttk.Frame(notebook, padding=PADDING)
        windows_tab.columnconfigure(0, weight=1)
        windows_tab.rowconfigure(0, weight=1)
        ttk.Button(
            windows_tab,
            text="Открыть дополнительное окно",
            command=self.open_info_window,
        ).grid(row=0, column=0)
        notebook.add(windows_tab, text="Несколько окон")

    def open_info_window(self) -> None:
        """Создаёт дополнительное окно с интерактивной кнопкой."""
        InfoWindow(self.root)

    def exit_application(self) -> None:
        """Закрывает главное окно и все дочерние окна."""
        self.root.destroy()
