"""
Ładowanie danych katalogu z folderu data/.

- systems.json — parametry techniczne systemów (redukcje cięcia, offsety,
  klasy wysokości, NL itd.).
- items/*.json — katalog SKU (drawer_set, connector, rail, lift, insert…),
  format zgodny z seedami kalkulatora: {sku, name, category, system_id, price, specs}.
"""
import json
import os
import glob
from functools import lru_cache

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(_HERE), "data")


@lru_cache(maxsize=1)
def load_systems():
    """Zwraca dict {system_id: {...parametry...}}."""
    with open(os.path.join(DATA_DIR, "systems.json"), encoding="utf-8") as f:
        return json.load(f)


def get_system(system_id):
    systems = load_systems()
    if system_id not in systems:
        raise KeyError(
            f"Nieznany system okuć: {system_id!r}. Dostępne: {sorted(systems)}"
        )
    return systems[system_id]


@lru_cache(maxsize=1)
def _load_all_items():
    items = []
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "items", "*.json"))):
        with open(path, encoding="utf-8") as f:
            items.extend(json.load(f))
    return items


def load_items(category=None, system_id=None):
    """Lista SKU (dict). Opcjonalny filtr po kategorii i/lub systemie."""
    items = _load_all_items()
    if category is not None:
        items = [it for it in items if it.get("category") == category]
    if system_id is not None:
        items = [it for it in items if it.get("system_id") == system_id]
    return items


def get_item(sku):
    return next((it for it in _load_all_items() if it.get("sku") == sku), None)
