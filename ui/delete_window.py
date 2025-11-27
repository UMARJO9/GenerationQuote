import customtkinter as ctk
from tkinter import messagebox
from ui.styles import COLORS, FONTS, BUTTON_STYLE


class DeleteWindow(ctk.CTkToplevel):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self.title("Удалить цитату")
        self.geometry("520x240")
        self.configure(fg_color=COLORS["background"])
        self.resizable(False, False)
        self.transient(self.master)
        self.grab_set()
        self.lift()
        self.focus_force()

        container = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel"],
            corner_radius=12,
            width=480,
            height=180
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            container,
            text="Выберите цитату для удаления",
            font=("Segoe UI Semibold", 12),
            text_color=COLORS["text"]
        ).place(x=22, y=22)

        self.quote_map = self._build_display_map()
        values = list(self.quote_map.keys()) or ["(нет цитат)"]

        self.combo = ctk.CTkComboBox(
            container,
            width=430,
            values=values,
            state="readonly" if values and values[0] != "(нет цитат)" else "disabled",
            fg_color=COLORS["panel"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            dropdown_fg_color=COLORS["panel"],
            dropdown_text_color=COLORS["text"],
            text_color=COLORS["text"],
            font=FONTS["base"]
        )
        self.combo.place(x=22, y=56)
        if values and values[0] != "(нет цитат)":
            self.combo.set(values[0])

        del_btn = ctk.CTkButton(
            container,
            text="Удалить",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="white",
            width=160,
            **BUTTON_STYLE,
            command=self.delete_selected
        )
        del_btn.place(relx=0.5, y=128, anchor="center")

    def _build_display_map(self):
        display = {}
        for q in self.repo.get_all():
            preview = (q.get("text") or "").strip()
            if len(preview) > 60:
                preview = preview[:57] + "..."
            label = f"{q.get('author','?')} — {preview}"
            # Ensure uniqueness if previews clash
            while label in display:
                label += " "
            display[label] = q.get("id")
        return display

    def delete_selected(self):
        if not self.quote_map:
            return
        selected = self.combo.get()
        quote_id = self.quote_map.get(selected)
        if not quote_id:
            messagebox.showerror("Ошибка", "Не выбрана цитата.")
            return
        if messagebox.askyesno("Удаление", "Удалить выбранную цитату?"):
            if self.repo.delete_quote(quote_id):
                messagebox.showinfo("Готово", "Цитата удалена.")
                self._reload_quotes()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить цитату.")

    def _reload_quotes(self):
        self.repo.quotes = self.repo.get_all()
        self.quote_map = self._build_display_map()
        values = list(self.quote_map.keys()) or ["(нет цитат)"]
        state = "readonly" if values and values[0] != "(нет цитат)" else "disabled"
        try:
            self.combo.configure(values=values, state=state)
        except Exception:
            self.combo.destroy()
            self.combo = ctk.CTkComboBox(
                self,
                width=430,
                values=values,
                state=state,
                fg_color=COLORS["panel"],
                button_color=COLORS["accent"],
                button_hover_color=COLORS["accent_hover"],
                dropdown_fg_color=COLORS["panel"],
                dropdown_text_color=COLORS["text"],
                text_color=COLORS["text"],
                font=FONTS["base"]
            )
            self.combo.place(x=22, y=56)
        if values and values[0] != "(нет цитат)":
            self.combo.set(values[0])
        else:
            self.combo.set("(нет цитат)")
