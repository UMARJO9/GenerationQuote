import uuid
from .data_loader import load_quotes, save_quotes

class QuoteRepository:
    def __init__(self, file_path="data/quotes.json"):
        self.file_path = file_path
        self.quotes = load_quotes(file_path)

    def get_all(self):
        return self.quotes

    def add_quote(self, text, author, categories):
        new_quote = {
            "id": f"q-{uuid.uuid4().hex[:8]}",
            "text": text.strip(),
            "author": author.strip(),
            "categories": categories
        }
        self.quotes.append(new_quote)
        save_quotes(self.file_path, self.quotes)
        return new_quote

    def delete_quote(self, quote_id: str) -> bool:
        before = len(self.quotes)
        self.quotes = [q for q in self.quotes if q.get("id") != quote_id]
        if len(self.quotes) < before:
            save_quotes(self.file_path, self.quotes)
            return True
        return False
