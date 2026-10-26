from dataclasses import dataclass, asdict
from typing import Optional

from .parse import parse_capacity_tb, parse_kind, parse_form


@dataclass
class Offer:
    source: str
    title: str
    price: float
    url: str
    image: Optional[str] = None
    original_price: Optional[float] = None
    brand: Optional[str] = None
    capacity_tb: Optional[float] = None
    kind: str = "HDD"
    form: str = "interno"

    @classmethod
    def build(cls, source, title, price, url, image=None, original_price=None, brand=None):
        return cls(
            source=source, title=title, price=float(price), url=url, image=image,
            original_price=float(original_price) if original_price else None,
            brand=brand, capacity_tb=parse_capacity_tb(title),
            kind=parse_kind(title), form=parse_form(title),
        )

    def to_dict(self):
        d = asdict(self)
        d["price_per_tb"] = round(self.price / self.capacity_tb, 2) if self.capacity_tb else None
        d["discount_pct"] = (
            round((1 - self.price / self.original_price) * 100, 1)
            if self.original_price and self.original_price > self.price else None
        )
        return d
