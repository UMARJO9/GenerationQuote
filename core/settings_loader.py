import json
from pathlib import Path


def _ensure_default_struct(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Некорректные настройки: ожидается объект с ключами 'authors' и 'categories'.")
    authors = data.get("authors", [])
    categories = data.get("categories", [])
    if not isinstance(authors, list) or not isinstance(categories, list):
        raise ValueError("Некорректные настройки: 'authors' и 'categories' должны быть списками.")
    return {"authors": authors, "categories": categories}


def load_settings(file_path: str):
    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"authors": [], "categories": []}', encoding="utf-8")
        return {"authors": [], "categories": []}

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return _ensure_default_struct(data)
        except json.JSONDecodeError:
            raise ValueError("Ошибка: повреждён JSON-файл настроек.")


def save_settings(file_path: str, settings: dict):
    # Валидация перед записью
    settings = _ensure_default_struct(settings)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

