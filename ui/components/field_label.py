import customtkinter as ctk
from ui.styles import COLORS

class FieldLabel(ctk.CTkLabel):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            text=text,
            font=("Segoe UI Semibold", 11),
            text_color=COLORS["text"]
        )
