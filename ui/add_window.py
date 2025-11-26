import customtkinter as ctk
from tkinter import messagebox
from ui.styles import COLORS
from ui.components.field_label import FieldLabel
from ui.components.text_field import TextField
from ui.components.input_field import InputField
from ui.components.save_button import SaveButton

class AddWindow(ctk.CTkToplevel):
    def __init__(self, repo):
        super().__init__()
        self.title("Добавить цитату")
        self.geometry("560x470")
        self.configure(fg_color=COLORS["background"])
        self.repo = repo
        self.resizable(False, False)

        frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=500,
            height=390
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")

        FieldLabel(frame, "Текст цитаты:").pack(pady=(10, 4))
        self.text_field = TextField(frame)
        self.text_field.pack(pady=(0, 8))

        FieldLabel(frame, "Автор:").pack(pady=(8, 4))
        self.author_field = InputField(frame)
        self.author_field.pack()

        FieldLabel(frame, "Категории (через запятую):").pack(pady=(8, 4))
        self.categories_field = InputField(frame)
        self.categories_field.pack()

        SaveButton(frame, self.save_quote).pack(pady=20)

    def save_quote(self):
        text = self.text_field.get()
        author = self.author_field.get_value()
        categories = [c.strip() for c in self.categories_field.get_value().split(",") if c.strip()]

        if not text or not author:
            messagebox.showerror("Ошибка", "Поля «Текст» и «Автор» обязательны.")
            return
        self.repo.add_quote(text, author, categories)
        self.repo.quotes = self.repo.get_all()

        messagebox.showinfo("✅ Успех", "Цитата добавлена!")
        self.destroy()

