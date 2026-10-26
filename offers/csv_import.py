import csv
import io
import os

from .base import Source
from .models import Offer

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "offerte.csv")
REQUIRED = ("prodotto", "prezzo")


def _num(value):
    value = (value or "").strip().replace("€", "").replace(" ", "")
    if not value:
        return None
    if "," in value:  # formato italiano: 1.299,90
        value = value.replace(".", "").replace(",", ".")
    return float(value)


def parse_csv(text, default_source="csv"):
    """Colonne: prodotto, prezzo (obbligatorie); fonte, prezzo_listino, url, tipo, forma, capacita_tb."""
    text = text.lstrip("﻿")
    first = text.split("\n", 1)[0]
    delim = ";" if first.count(";") > first.count(",") else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delim)
    reader.fieldnames = [(f or "").strip().lower() for f in reader.fieldnames or []]
    missing = [c for c in REQUIRED if c not in reader.fieldnames]
    if missing:
        raise ValueError("colonne mancanti: " + ", ".join(missing))
    offers = []
    for n, row in enumerate(reader, start=2):
        try:
            price = _num(row["prezzo"])
            if not row["prodotto"].strip() or price is None:
                raise ValueError("prodotto o prezzo vuoto")
            offers.append(Offer.build(
                (row.get("fonte") or default_source).strip(), row["prodotto"].strip(), price,
                (row.get("url") or "").strip(), original_price=_num(row.get("prezzo_listino")),
                kind=(row.get("tipo") or "").strip().upper() or None,
                form=(row.get("forma") or "").strip().lower() or None,
                capacity_tb=_num(row.get("capacita_tb")),
            ))
        except ValueError as e:
            raise ValueError(f"riga {n}: {e}")
    return offers


class CsvSource(Source):
    """Legge data/offerte.csv (modificabile a mano)."""
    name = "csv"

    def __init__(self, path=DEFAULT_PATH):
        self.path = path

    def available(self):
        return os.path.exists(self.path)

    def search(self, query, limit=200):
        with open(self.path, encoding="utf-8") as f:
            offers = parse_csv(f.read())
        words = query.lower().split()
        return [o for o in offers if all(w in o.title.lower() or w in o.source.lower() for w in words)][:limit]
