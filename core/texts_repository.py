from .texts_loader import load_texts


class TextsRepository:
    def __init__(self, file_path="data/texts.json"):
        self.file_path = file_path
        self.texts = load_texts(file_path)

    def reload(self):
        self.texts = load_texts(self.file_path)
        return self.texts

    def get(self, key: str, default: str | None = None) -> str:
        parts = key.split('.') if key else []
        node = self.texts
        for p in parts:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                return default if default is not None else key
        if isinstance(node, str):
            return node
        return default if default is not None else key

