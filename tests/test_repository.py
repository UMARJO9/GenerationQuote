from core.repository import QuoteRepository
import json

def test_add_and_get_quotes(tmp_path):
    file = tmp_path / "quotes.json"
    repo = QuoteRepository(file)
    repo.add_quote("Тест", "Автор", ["категория"])
    data = json.loads(file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["text"] == "Тест"
