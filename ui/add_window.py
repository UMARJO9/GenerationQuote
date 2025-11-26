import customtkinter as ctk
from tkinter import messagebox
from ui.styles import COLORS, FONTS
from ui.components.field_label import FieldLabel
from ui.components.text_field import TextField
from ui.components.save_button import SaveButton
from core.settings_repository import SettingsRepository
from core.texts_repository import TextsRepository


class AddWindow(ctk.CTkToplevel):
    def __init__(self, repo, settings_repo: SettingsRepository | None = None):
        super().__init__()
        self.texts = TextsRepository()
        t = self.texts.get
        self.title(t("add.title"))
        self.geometry("560x520")
        self.configure(fg_color=COLORS["background"])
        self.repo = repo
        self.settings_repo = settings_repo or SettingsRepository()
        self.resizable(False, False)

        frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=500,
            height=440
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Текст цитаты
        FieldLabel(frame, t("add.fields.quote")).pack(pady=(10, 4))
        self.text_field = TextField(frame)
        self.text_field.pack(pady=(0, 8))

        # Автор из настроек
        FieldLabel(frame, t("add.fields.author")).pack(pady=(8, 4))
        self.settings_repo.reload()
        authors = self.settings_repo.get_authors()
        self.author_combo = ctk.CTkComboBox(frame, width=420, values=authors)
        self.author_combo.pack()

        # Множественный выбор категорий
        FieldLabel(frame, t("add.fields.categories")).pack(pady=(8, 4))
        categories = self.settings_repo.get_categories()
        self.categories_box = ctk.CTkScrollableFrame(frame, width=420, height=150, fg_color=COLORS["panel"], corner_radius=8)
        self.categories_box.pack()
        self.category_checks = []
        for idx, title in enumerate(categories):
            cb = ctk.CTkCheckBox(self.categories_box, text=title, font=FONTS["base"])
            cb.pack(anchor="w", pady=(6 if idx == 0 else 0, 6), padx=8)
            self.category_checks.append((title, cb))

        SaveButton(frame, self.save_quote, text=t("add.save_button")).pack(pady=20)

    def save_quote(self):
        t = self.texts.get
        text = self.text_field.get()
        author = (self.author_combo.get() or "").strip()
        categories = [title for title, cb in self.category_checks if cb.get() == 1]

        if not text or not author:
            messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.message"))
            return

        self.repo.add_quote(text, author, categories)
        self.repo.quotes = self.repo.get_all()

        messagebox.showinfo(t("add.save_success.title"), t("add.save_success.message"))
        self.destroy()



