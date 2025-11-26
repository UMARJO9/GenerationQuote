import customtkinter as ctk
from tkinter import messagebox
from ui.styles import COLORS, FONTS
from ui.components.field_label import FieldLabel
from ui.components.text_field import TextField
from ui.components.save_button import SaveButton
from core.settings_repository import SettingsRepository
from core.texts_repository import TextsRepository
from ui.settings_window import SettingsWindow


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
        self.form_frame = frame

        # Текст цитаты
        FieldLabel(frame, t("add.fields.quote")).pack(pady=(10, 4))
        self.text_field = TextField(frame)
        self.text_field.pack(pady=(0, 8))

        # Автор из настроек
        FieldLabel(frame, t("add.fields.author")).pack(pady=(8, 4))
        self.settings_repo.reload()
        authors = self.settings_repo.get_authors()
        self.author_combo = ctk.CTkComboBox(frame, width=420, values=authors, state="readonly")
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
        raw_text = self.text_field.get()
        text = (raw_text or "").strip()
        author = (self.author_combo.get() or "").strip()
        categories = [title for title, cb in self.category_checks if cb.get() == 1]

        # Получаем справочники
        authors_ref = set(a.lower() for a in self.settings_repo.get_authors())
        categories_ref = set(c.lower() for c in self.settings_repo.get_categories())

        # Валидации текста
        if not text:
            messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.missing_text"))
            return
        if len(text) < 5:
            messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.text_too_short"))
            return
        if len(text) > 600:
            messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.text_too_long"))
            return

        # Валидации автора
        if not author:
            if messagebox.askyesno(t("add.prompts.open_settings.title"), t("add.prompts.open_settings.open_settings_author")):
                win = SettingsWindow(self.settings_repo)
                self.wait_window(win)
                self.refresh_authors()
            else:
                messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.missing_author"))
            return
        if author.lower() not in authors_ref:
            if messagebox.askyesno(t("add.prompts.open_settings.title"), t("add.prompts.open_settings.open_settings_author")):
                win = SettingsWindow(self.settings_repo)
                self.wait_window(win)
                self.refresh_authors()
            else:
                messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.author_not_in_list"))
            return

        # Валидации категорий
        if not categories:
            if messagebox.askyesno(t("add.prompts.open_settings.title"), t("add.prompts.open_settings.open_settings_category")):
                win = SettingsWindow(self.settings_repo)
                self.wait_window(win)
                self.refresh_categories()
            else:
                messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.missing_categories"))
            return
        invalid = [c for c in categories if c.lower() not in categories_ref]
        if invalid:
            if messagebox.askyesno(t("add.prompts.open_settings.title"), t("add.prompts.open_settings.open_settings_category")):
                win = SettingsWindow(self.settings_repo)
                self.wait_window(win)
                self.refresh_categories()
            else:
                messagebox.showerror(t("add.validation_error.title"), t("add.validation_error.category_not_in_list"))
            return

        # Проверка дубликатов (по тексту и автору, без учета регистра и пробелов)
        norm = lambda s: (s or "").strip().lower()
        for q in self.repo.get_all():
            if norm(q.get("text")) == norm(text) and norm(q.get("author")) == norm(author):
                messagebox.showwarning(t("add.validation_error.title"), t("add.validation_error.duplicate_quote"))
                return

        # Запись
        self.repo.add_quote(text, author, categories)
        self.repo.quotes = self.repo.get_all()

        messagebox.showinfo(t("add.save_success.title"), t("add.save_success.message"))
        self.destroy()

    def refresh_authors(self):
        # Reload authors and repopulate combobox
        self.settings_repo.reload()
        authors = self.settings_repo.get_authors()
        try:
            self.author_combo.configure(values=authors)
            self.author_combo.set("")
        except Exception:
            # Recreate if needed
            self.author_combo.destroy()
            self.author_combo = ctk.CTkComboBox(self.form_frame, width=420, values=authors, state="readonly")
            self.author_combo.pack()

    def refresh_categories(self):
        # Reload categories and rebuild checkboxes
        self.settings_repo.reload()
        categories = self.settings_repo.get_categories()
        try:
            for _, cb in self.category_checks:
                cb.destroy()
        except Exception:
            pass
        self.category_checks = []
        for idx, title in enumerate(categories):
            cb = ctk.CTkCheckBox(self.categories_box, text=title, font=FONTS["base"])
            cb.pack(anchor="w", pady=(6 if idx == 0 else 0, 6), padx=8)
            self.category_checks.append((title, cb))



