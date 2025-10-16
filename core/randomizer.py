import random

def random_quote(quotes, category=None):
    if not quotes:
        raise ValueError("Нет доступных цитат.")
    if category:
        filtered = [q for q in quotes if category in q.get("categories", [])]
        if not filtered:
            raise ValueError(f"Нет цитат в категории '{category}'.")
        return random.choice(filtered)
    return random.choice(quotes)
