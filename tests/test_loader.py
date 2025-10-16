import pytest
from core.data_loader import load_quotes, save_quotes

def test_load_and_save_quotes(tmp_path):
    file = tmp_path / "quotes.json"
    sample_data = [{"id": "q1", "text": "Hello", "author": "Anon", "categories": []}]
    save_quotes(file, sample_data)

    loaded = load_quotes(file)
    assert len(loaded) == 1
    assert loaded[0]["text"] == "Hello"

def test_load_invalid_json(tmp_path):
    file = tmp_path / "broken.json"
    file.write_text("{bad json}")
    with pytest.raises(ValueError):
        load_quotes(file)
