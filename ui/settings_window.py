import customtkinter as ctk
from tkinter import messagebox
from ui.styles import COLORS, FONTS, BUTTON_STYLE


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, repo):
        super().__init__()
        self.title("Настройки")
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

        # Authors section
        authors_label = ctk.CTkLabel(container, text="Авторы", font=("Segoe UI Semibold", 12), text_color=COLORS["text"])        
        authors_label.place(x=24, y=18)

        self.author_entry = ctk.CTkEntry(container, width=240, font=FONTS["base"], fg_color=COLORS["panel"], text_color="#1e293b")
        self.author_entry.place(x=24, y=48)

        add_author_btn = ctk.CTkButton(container, text="Добавить", width=110, command=self.add_author, fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], text_color="white", **BUTTON_STYLE)
        add_author_btn.place(x=276, y=46)

        self.author_combo = ctk.CTkComboBox(container, width=240, values=self.repo.get_authors())
        self.author_combo.place(x=24, y=92)

        del_author_btn = ctk.CTkButton(container, text="Удалить", width=110, command=self.delete_author, fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"], text_color="white", **BUTTON_STYLE)
        del_author_btn.place(x=276, y=90)

        # Categories section
        categories_label = ctk.CTkLabel(container, text="Категории", font=("Segoe UI Semibold", 12), text_color=COLORS["text"])        
        categories_label.place(x=24, y=150)

        self.category_entry = ctk.CTkEntry(container, width=240, font=FONTS["base"], fg_color=COLORS["panel"], text_color="#1e293b")
        self.category_entry.place(x=24, y=180)

        add_category_btn = ctk.CTkButton(container, text="Добавить", width=110, command=self.add_category, fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], text_color="white", **BUTTON_STYLE)
        add_category_btn.place(x=276, y=178)

        self.category_combo = ctk.CTkComboBox(container, width=240, values=self.repo.get_categories())
        self.category_combo.place(x=24, y=224)

        del_category_btn = ctk.CTkButton(container, text="Удалить", width=110, command=self.delete_category, fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"], text_color="white", **BUTTON_STYLE)
        del_category_btn.place(x=276, y=222)

        close_btn = ctk.CTkButton(container, text="Закрыть", width=120, command=self.destroy, fg_color="#64748b", hover_color="#475569", text_color="white", **BUTTON_STYLE)
        close_btn.place(relx=0.5, y=312, anchor="center")

    def refresh_lists(self):
        self.repo.reload()
        self.author_combo.configure(values=self.repo.get_authors())
        self.category_combo.configure(values=self.repo.get_categories())

    def add_author(self):
        name = self.author_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите имя автора.")
            return
        if not self.repo.add_author(name):
            messagebox.showwarning("Внимание", "Такой автор уже есть или имя пустое.")
        else:
            self.author_entry.delete(0, "end")
            self.refresh_lists()

    def delete_author(self):
        name = (self.author_combo.get() or "").strip()
        if not name:
            messagebox.showerror("Ошибка", "Выберите автора для удаления.")
            return
        if self.repo.delete_author(name):
            self.refresh_lists()
        else:
            messagebox.showwarning("Внимание", "Автор не найден.")

    def add_category(self):
        title = self.category_entry.get().strip()
        if not title:
            messagebox.showerror("Ошибка", "Введите название категории.")
            return
        if not self.repo.add_category(title):
            messagebox.showwarning("Внимание", "Такая категория уже есть или название пустое.")
        else:
            self.category_entry.delete(0, "end")
            self.refresh_lists()

    def delete_category(self):
        title = (self.category_combo.get() or "").strip()
        if not title:
            messagebox.showerror("Ошибка", "Выберите категорию для удаления.")
            return
        if self.repo.delete_category(title):
            self.refresh_lists()
        else:
            messagebox.showwarning("Внимание", "Категория не найдена.")

