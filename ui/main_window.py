import customtkinter as ctk
from core.repository import QuoteRepository
from core.randomizer import random_quote
from ui.add_window import AddWindow
from ui.styles import COLORS, FONTS, BUTTON_STYLE
from core.settings_repository import SettingsRepository
from ui.settings_window import SettingsWindow
from core.texts_repository import TextsRepository


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("640x520")
        self.texts = TextsRepository()
        t = self.texts.get
        self.title(t("app.title"))
        self.configure(fg_color=COLORS["background"])

        self.repo = QuoteRepository()
        self.settings_repo = SettingsRepository()

        self.selected_authors: set[str] = set()
        self.selected_categories: set[str] = set()

        # Фильтры (левая карточка, фиксированная высота)
        filters_container = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=360,
            height=150,
            border_width=1,
            border_color="#e5e7eb"
        )
        filters_container.place(x=16, y=20)

        self.filters_box = ctk.CTkScrollableFrame(
            filters_container,
            fg_color=COLORS["panel"],
            corner_radius=10,
            width=348,
            height=142,
            scrollbar_fg_color=COLORS["panel"],
            scrollbar_button_color=COLORS["accent"],
            scrollbar_button_hover_color=COLORS["accent_hover"]
        )
        self.filters_box.place(x=6, y=4)

        filters_title = ctk.CTkLabel(
            self.filters_box,
            text="Фильтры",
            font=("Segoe UI Semibold", 11),
            text_color=COLORS["text"]
        )
        filters_title.pack(anchor="w", padx=10, pady=(4, 6))

        filters_row = ctk.CTkFrame(self.filters_box, fg_color=COLORS["panel"])
        filters_row.pack(fill="x", padx=8, pady=(0, 6))

        left_col = ctk.CTkFrame(filters_row, fg_color=COLORS["panel"])
        left_col.grid(row=0, column=0, padx=(0, 12), sticky="nw")

        right_col = ctk.CTkFrame(filters_row, fg_color=COLORS["panel"])
        right_col.grid(row=0, column=1, sticky="nw")

        author_label = ctk.CTkLabel(left_col, text="Авторы", font=FONTS["base"], text_color=COLORS["text"])
        author_label.pack(anchor="w")
        self.authors_box = ctk.CTkFrame(left_col, fg_color=COLORS["panel"])
        self.authors_box.pack(anchor="w", pady=(4, 0))

        category_label = ctk.CTkLabel(right_col, text="Категории", font=FONTS["base"], text_color=COLORS["text"])
        category_label.pack(anchor="w")
        self.categories_box = ctk.CTkFrame(right_col, fg_color=COLORS["panel"])
        self.categories_box.pack(anchor="w", pady=(4, 0))

        self.build_filter_checkboxes()

        # Кнопки (правая карточка, такая же высота)
        actions_box = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=220,
            height=150,
            border_width=1,
            border_color="#e5e7eb"
        )
        actions_box.place(relx=1, x=-16, y=20, anchor="ne")

        add_btn = ctk.CTkButton(
            actions_box,
            text=t("main.add_button"),
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            text_color="white",
            width=150,
            **BUTTON_STYLE,
            command=self.open_add_window
        )
        add_btn.place(relx=0.5, y=38, anchor="center")

        settings_btn = ctk.CTkButton(
            actions_box,
            text="⚙",
            fg_color=COLORS["panel"],
            hover_color="#e5e7eb",
            text_color=COLORS["text"],
            width=44,
            height=36,
            corner_radius=8,
            command=self.open_settings
        )
        settings_btn.place(relx=0.5, y=98, anchor="center")

        self.quote_label = ctk.CTkLabel(
            self,
            text=t("main.placeholder_quote"),
            wraplength=520,
            justify="center",
            font=FONTS["quote"],
            text_color=COLORS["text"]
        )
        self.quote_label.place(relx=0.5, rely=0.62, anchor="center")

        gen_btn = ctk.CTkButton(
            self,
            text=t("main.generate_button"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="white",
            width=220,
            **BUTTON_STYLE,
            command=self.generate_quote
        )
        gen_btn.place(relx=0.5, rely=0.9, anchor="center")

        footer = ctk.CTkLabel(
            self,
            text=t("app.footer"),
            text_color=COLORS["text"],
            font=FONTS["small"]
        )
        footer.place(relx=0.5, rely=0.96, anchor="center")

        # Прокрутка только внутри блока фильтров
        self.bind_all("<MouseWheel>", self._on_mousewheel_filters, add="+")

    def generate_quote(self):
        try:
            quote = random_quote(
                self.repo.quotes,
                authors=self.selected_authors,
                categories=self.selected_categories
            )
            text = f"\"{quote['text']}\"\n\n- {quote['author']}"
            self.quote_label.configure(text=text)
        except ValueError as e:
            self.quote_label.configure(text=str(e))

    def open_add_window(self):
        win = AddWindow(self.repo, self.settings_repo)
        self.wait_window(win)
        self.repo.quotes = self.repo.get_all()
        self.refresh_filters()

    def open_settings(self):
        win = SettingsWindow(self.settings_repo)
        self.wait_window(win)
        self.refresh_filters()

    def build_filter_checkboxes(self):
        # Authors
        old_authors = set(self.selected_authors)
        for child in self.authors_box.winfo_children():
            child.destroy()
        self.selected_authors = set()
        for name in self.settings_repo.get_authors():
            cb = ctk.CTkCheckBox(
                self.authors_box,
                text=name,
                font=FONTS["base"],
                text_color=COLORS["text"],
                command=lambda n=name: self.toggle_author(n)
            )
            cb.pack(anchor="w", padx=6, pady=2)
            if name in old_authors:
                cb.select()
                self.selected_authors.add(name)

        # Categories
        old_categories = set(self.selected_categories)
        for child in self.categories_box.winfo_children():
            child.destroy()
        self.selected_categories = set()
        for cat in self.settings_repo.get_categories():
            cb = ctk.CTkCheckBox(
                self.categories_box,
                text=cat,
                font=FONTS["base"],
                text_color=COLORS["text"],
                command=lambda c=cat: self.toggle_category(c)
            )
            cb.pack(anchor="w", padx=6, pady=2)
            if cat in old_categories:
                cb.select()
                self.selected_categories.add(cat)

    def toggle_author(self, name: str):
        if name in self.selected_authors:
            self.selected_authors.remove(name)
        else:
            self.selected_authors.add(name)

    def toggle_category(self, title: str):
        if title in self.selected_categories:
            self.selected_categories.remove(title)
        else:
            self.selected_categories.add(title)

    def refresh_filters(self):
        self.settings_repo.reload()
        self.build_filter_checkboxes()

    def _on_mousewheel_filters(self, event):
        if self._pointer_in_filters_area():
            canvas = getattr(self.filters_box, "_parent_canvas", None)
            if canvas:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

    def _pointer_in_filters_area(self) -> bool:
        try:
            widget = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
        except Exception:
            return False
        while widget:
            if widget == self.filters_box:
                return True
            widget = getattr(widget, "master", None)
        return False
