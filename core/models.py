from dataclasses import dataclass
from typing import List

@dataclass
class Quote:
    id: str
    text: str
    author: str
    categories: List[str]