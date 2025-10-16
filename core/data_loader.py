import json
from pathlib import Path

def load_quotes(file_path: str):
    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('[]', encoding="utf-8")
        return []

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Неверный формат: ожидается список цитат.")
            return data
        except json.JSONDecodeError:
            raise ValueError("Ошибка: повреждён JSON-файл.")

def save_quotes(file_path: str, quotes: list):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)
