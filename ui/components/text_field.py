import customtkinter as ctk
from ui.styles import COLORS, FONTS


class TextField(ctk.CTkFrame):
    def __init__(self, parent, width=420, height=90):
        super().__init__(
            parent,
            fg_color="#d1d5db",
            corner_radius=8
        )

        self.text_widget = ctk.CTkTextbox(
            self,
            width=width,
            height=height,
            font=FONTS["base"],
            fg_color=COLORS["panel"],
            text_color="#1e293b",
            corner_radius=8
        )
        self.text_widget.pack(padx=1, pady=1)

    def get(self):
        return self.text_widget.get("1.0", "end").strip()

    def clear(self):
        self.text_widget.delete("1.0", "end")
