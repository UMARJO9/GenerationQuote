import customtkinter as ctk
from core.repository import QuoteRepository
from core.randomizer import random_quote
from ui.add_window import AddWindow
from ui.styles import COLORS, FONTS, BUTTON_STYLE

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("640x520")
        self.title("Генератор афоризмов и цитат")
        self.configure(fg_color=COLORS["background"])

        self.repo = QuoteRepository()

        top_bar = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=600,
            height=60
        )
        top_bar.place(relx=0.5, y=40, anchor="center")

        gen_btn = ctk.CTkButton(
            top_bar,
            text="🎲 Сгенерировать",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="white",
            width=180,
            **BUTTON_STYLE,
            command=self.generate_quote
        )
        gen_btn.place(x=20, y=12)

        add_btn = ctk.CTkButton(
            top_bar,
            text="➕ Добавить",
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            text_color="white",
            width=180,
            **BUTTON_STYLE,
            command=self.open_add_window
        )
        add_btn.place(x=400, y=12)

        self.quote_label = ctk.CTkLabel(
            self,
            text="Нажмите «Сгенерировать» для получения цитаты",
            wraplength=520,
            justify="center",
            font=FONTS["quote"],
            text_color=COLORS["text"]
        )
        self.quote_label.place(relx=0.5, rely=0.52, anchor="center")

        footer = ctk.CTkLabel(
            self,
            text="© Umarjon Nurmadov",
            text_color="#6b7280",
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
        win = AddWindow(self.repo)
        self.wait_window(win)
        self.repo.quotes = self.repo.get_all()



