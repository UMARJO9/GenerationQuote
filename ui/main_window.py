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

        top_right = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=230,
            height=52
        )
        top_right.place(relx=1, x=-16, y=28, anchor="ne")

        add_btn = ctk.CTkButton(
            top_right,
            text=t("main.add_button"),
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            text_color="white",
            width=140,
            **BUTTON_STYLE,
            command=self.open_add_window
        )
        add_btn.place(x=10, y=8)

        settings_btn = ctk.CTkButton(
            top_right,
            text="⚙",
            fg_color=COLORS["panel"],
            hover_color="#e5e7eb",
            text_color=COLORS["text"],
            width=46,
            height=36,
            corner_radius=8,
            command=self.open_settings
        )
        settings_btn.place(x=170, y=8)

        self.quote_label = ctk.CTkLabel(
            self,
            text=t("main.placeholder_quote"),
            wraplength=520,
            justify="center",
            font=FONTS["quote"],
            text_color=COLORS["text"]
        )
        self.quote_label.place(relx=0.5, rely=0.55, anchor="center")

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
        gen_btn.place(relx=0.5, rely=0.82, anchor="center")

        footer = ctk.CTkLabel(
            self,
            text=t("app.footer"),
            text_color=COLORS["text"],
            font=FONTS["small"]
        )
        footer.place(relx=0.5, rely=0.96, anchor="center")

    def generate_quote(self):
        try:
            quote = random_quote(self.repo.quotes)
            text = f"\"{quote['text']}\"\n\n- {quote['author']}"
            self.quote_label.configure(text=text)
        except ValueError as e:
            self.quote_label.configure(text=str(e))

    def open_add_window(self):
        win = AddWindow(self.repo, self.settings_repo)
        self.wait_window(win)
        self.repo.quotes = self.repo.get_all()

    def open_settings(self):
        win = SettingsWindow(self.settings_repo)
        self.wait_window(win)
