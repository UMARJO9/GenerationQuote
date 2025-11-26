import customtkinter as ctk
from tkinter import messagebox
from ui.styles import COLORS, FONTS, BUTTON_STYLE
from core.texts_repository import TextsRepository


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, repo):
        super().__init__()
        self.texts = TextsRepository()
        t = self.texts.get
        self.title(t("settings.title"))
        self.geometry("600x420")
        self.configure(fg_color=COLORS["background"])        
        self.repo = repo
        self.resizable(False, False)

        container = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=560,
            height=360
        )
        container.place(relx=0.5, rely=0.5, anchor="center")
        self.container = container

        # Authors section
        authors_label = ctk.CTkLabel(container, text=t("settings.sections.authors"), font=("Segoe UI Semibold", 12), text_color=COLORS["text"])        
        authors_label.place(x=24, y=18)

        self.author_entry = ctk.CTkEntry(container, width=240, font=FONTS["base"], fg_color=COLORS["panel"], text_color="#1e293b")
        self.author_entry.place(x=24, y=48)

        add_author_btn = ctk.CTkButton(container, text=t("settings.buttons.add"), width=110, command=self.add_author, fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], text_color="white", **BUTTON_STYLE)
        add_author_btn.place(x=276, y=46)

        self.author_combo = ctk.CTkComboBox(container, width=240, values=self.repo.get_authors())
        self.author_combo.place(x=24, y=92)

        del_author_btn = ctk.CTkButton(container, text=t("settings.buttons.delete"), width=110, command=self.delete_author, fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"], text_color="white", **BUTTON_STYLE)
        del_author_btn.place(x=276, y=90)

        # Categories section
        categories_label = ctk.CTkLabel(container, text=t("settings.sections.categories"), font=("Segoe UI Semibold", 12), text_color=COLORS["text"])        
        categories_label.place(x=24, y=150)

        self.category_entry = ctk.CTkEntry(container, width=240, font=FONTS["base"], fg_color=COLORS["panel"], text_color="#1e293b")
        self.category_entry.place(x=24, y=180)

        add_category_btn = ctk.CTkButton(container, text=t("settings.buttons.add"), width=110, command=self.add_category, fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], text_color="white", **BUTTON_STYLE)
        add_category_btn.place(x=276, y=178)

        self.category_combo = ctk.CTkComboBox(container, width=240, values=self.repo.get_categories())
        self.category_combo.place(x=24, y=224)

        del_category_btn = ctk.CTkButton(container, text=t("settings.buttons.delete"), width=110, command=self.delete_category, fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"], text_color="white", **BUTTON_STYLE)
        del_category_btn.place(x=276, y=222)

        close_btn = ctk.CTkButton(container, text=t("settings.buttons.close"), width=120, command=self.destroy, fg_color="#64748b", hover_color="#475569", text_color="white", **BUTTON_STYLE)
        close_btn.place(relx=0.5, y=312, anchor="center")

    def refresh_lists(self):
        self.repo.reload()
        authors = self.repo.get_authors()
        categories = self.repo.get_categories()
        # Полное пересоздание комбобоксов, чтобы меню наверняка обновилось
        try:
            self.author_combo.destroy()
        except Exception:
            pass
        self.author_combo = ctk.CTkComboBox(self.container, width=240, values=authors)
        self.author_combo.place(x=24, y=92)

        try:
            self.category_combo.destroy()
        except Exception:
            pass
        self.category_combo = ctk.CTkComboBox(self.container, width=240, values=categories)
        self.category_combo.place(x=24, y=224)

    def add_author(self):
        t = self.texts.get
        name = self.author_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", t("settings.errors.enter_author"))
            return
        if not self.repo.add_author(name):
            messagebox.showwarning("Внимание", t("settings.warnings.author_exists"))
        else:
            self.author_entry.delete(0, "end")
            self.refresh_lists()

    def delete_author(self):
        t = self.texts.get
        name = (self.author_combo.get() or "").strip()
        if not name:
            messagebox.showerror("Ошибка", t("settings.errors.select_author"))
            return
        if self.repo.delete_author(name):
            self.refresh_lists()
        else:
            messagebox.showwarning("Внимание", t("settings.warnings.author_not_found"))

    def add_category(self):
        t = self.texts.get
        title = self.category_entry.get().strip()
        if not title:
            messagebox.showerror("Ошибка", t("settings.errors.enter_category"))
            return
        if not self.repo.add_category(title):
            messagebox.showwarning("Внимание", t("settings.warnings.category_exists"))
        else:
            self.category_entry.delete(0, "end")
            self.refresh_lists()

    def delete_category(self):
        t = self.texts.get
        title = (self.category_combo.get() or "").strip()
        if not title:
            messagebox.showerror("Ошибка", t("settings.errors.select_category"))
            return
        if self.repo.delete_category(title):
            self.refresh_lists()
        else:
            messagebox.showwarning("Внимание", t("settings.warnings.category_not_found"))
