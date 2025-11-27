import random
from typing import Iterable, Sequence


def random_quote(
    quotes: Sequence[dict],
    authors: Iterable[str] | None = None,
    categories: Iterable[str] | None = None
):
    if not quotes:
        raise ValueError("Нет цитат в базе.")

    authors_set = {a for a in authors or [] if a}
    categories_set = {c for c in categories or [] if c}

    def matches(q: dict) -> bool:
        if authors_set and q.get("author") not in authors_set:
            return False
        if categories_set:
            quote_cats = set(q.get("categories", []))
            return bool(quote_cats.intersection(categories_set))
        return True

    filtered = [q for q in quotes if matches(q)]
    if not filtered:
        raise ValueError("По выбранным фильтрам цитат нет.")
    return random.choice(filtered)
