import customtkinter as ctk
from ui.styles import COLORS, FONTS

class InputField(ctk.CTkEntry):
    def __init__(self, parent, width=420):
        super().__init__(
            parent,
            width=width,
            font=FONTS["base"],
            fg_color=COLORS["panel"],
            text_color="#1e293b",
            corner_radius=8,
            border_width=1,
            border_color="#d1d5db"
        )

    def get_value(self):
        return self.get().strip()

    def clear(self):
        self.delete(0, "end")
