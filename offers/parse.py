import re

_CAP = re.compile(r"(\d+(?:[.,]\d+)?)\s*(TB|TO|T|GB|GO|G)\b", re.I)


def parse_capacity_tb(title):
    """Estrae la capacità dal titolo e la restituisce in TB (None se assente)."""
    for value, unit in _CAP.findall(title):
        n = float(value.replace(",", "."))
        tb = n if unit.upper() in ("TB", "TO", "T") else n / 1000
        if 0.1 <= tb <= 100:
            return tb
    return None


def parse_kind(title):
    t = title.lower()
    if "nvme" in t or "m.2" in t:
        return "SSD"
    if "ssd" in t:
        return "SSD"
    if "nas" in t:
        return "NAS"
    if any(k in t for k in ("hdd", "hard disk", "hard drive", "barracuda", "ironwolf", "wd blue", "red plus")):
        return "HDD"
    return "HDD"


def parse_form(title):
    t = title.lower()
    if any(k in t for k in ("esterno", "external", "portatile", "portable", "passport", "elements", "my passport")):
        return "esterno"
    return "interno"
