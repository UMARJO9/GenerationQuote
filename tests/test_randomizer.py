import pytest
from core.randomizer import random_quote

def test_random_quote_from_list():
    quotes = [{"text": "A"}, {"text": "B"}, {"text": "C"}]
    result = random_quote(quotes)
    assert result["text"] in ["A", "B", "C"]

def test_random_quote_empty_list():
    with pytest.raises(ValueError):
        random_quote([])
