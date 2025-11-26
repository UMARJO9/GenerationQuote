import json
from pathlib import Path


DEFAULT_TEXTS = {
    "app": {
        "title": "Генератор цитат",
        "footer": "© Umarjon Nurmadov"
    },
    "main": {
        "generate_button": "Сгенерировать",
        "add_button": "Добавить",
        "placeholder_quote": "Нажмите «Сгенерировать» для получения цитаты"
    },
    "add": {
        "title": "Добавление цитаты",
        "fields": {
            "quote": "Текст цитаты:",
            "author": "Автор:",
            "categories": "Категории (можно несколько):"
        },
        "validation_error": {
            "title": "Ошибка",
            "message": "Текст и автор обязательны.",
            "missing_text": "Введите текст цитаты.",
            "missing_author": "Выберите автора из списка.",
            "missing_categories": "Выберите хотя бы одну категорию.",
            "text_too_short": "Текст слишком короткий.",
            "text_too_long": "Текст слишком длинный.",
            "author_not_in_list": "Укажите автора из настроек.",
            "category_not_in_list": "Некоторые категории отсутствуют в настройках.",
            "duplicate_quote": "Такая цитата с этим автором уже существует."
        },
        "save_success": {
            "title": "Готово",
            "message": "Цитата сохранена!"
        },
        "save_button": "Сохранить"
    },
    "settings": {
        "title": "Настройки",
        "sections": {
            "authors": "Авторы",
            "categories": "Категории"
        },
        "buttons": {
            "add": "Добавить",
            "delete": "Удалить",
            "close": "Закрыть"
        },
        "errors": {
            "enter_author": "Введите имя автора.",
            "enter_category": "Введите название категории.",
            "select_author": "Выберите автора для удаления.",
            "select_category": "Выберите категорию для удаления."
        },
        "warnings": {
            "author_exists": "Такой автор уже есть или имя пустое.",
            "category_exists": "Такая категория уже есть или название пустое.",
            "author_not_found": "Автор не найден.",
            "category_not_found": "Категория не найдена."
        }
    }
}


def load_texts(file_path: str):
    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(DEFAULT_TEXTS, ensure_ascii=False, indent=2), encoding="utf-8")
        return DEFAULT_TEXTS
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            # Если файл повреждён, вернём дефолтные строки
            return DEFAULT_TEXTS


def save_texts(file_path: str, texts: dict):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)
