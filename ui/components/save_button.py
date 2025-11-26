import customtkinter as ctk
from ui.styles import COLORS, BUTTON_STYLE

class SaveButton(ctk.CTkButton):
    def __init__(self, parent, command, text: str = "Сохранить"):
        super().__init__(
            parent,
            text=text,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="white",
            width=160,
            **BUTTON_STYLE,
            command=command
        )


