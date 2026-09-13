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


@lru_cache(maxsize=1)
def load_hinge_systems():
    """Zwraca dict {hinge_system_id: {...}} z hinge_systems.json."""
    path = os.path.join(DATA_DIR, "hinge_systems.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_drawer_system_by_name(name):
    """Wyszukuje system szuflad po polu `name` (np. 'GTV Axis Pro'). None gdy brak."""
    return next((s for s in load_systems().values() if s.get("name") == name), None)


def get_hinge_system_by_name(name):
    """Wyszukuje system zawiasów po polu `name` (np. 'Blum Clip Top'). None gdy brak."""
    return next((s for s in load_hinge_systems().values() if s.get("name") == name), None)


def resolve_system_id(name_or_id):
    """Zwraca id systemu szuflad. Przyjmuje gotowe id (np. 'gtv_axis_pro') albo
    nazwę (np. 'GTV Axis Pro'). None gdy nie rozpoznano."""
    systems = load_systems()
    if name_or_id in systems:
        return name_or_id
    found = get_drawer_system_by_name(name_or_id)
    return found["id"] if found else None


# --------------------------------------------------------------------------
# DOKUMENTY PRODUCENTÓW
# --------------------------------------------------------------------------
#
# Katalog trzymał dotąd WARTOŚCI wyjęte z kart producenta (`source_pdf`,
# `source_page`) i nie trzymał samych kart. Liczba bez dokumentu jest nie do
# sprawdzenia, a stolarz przy maszynie i tak potrzebuje rysunku montażowego,
# a nie tabelki — stąd `dokumenty/` obok `data/`.
#
# Dokument należy do SYSTEMU albo do SKU, nigdy do pojedynczej pozycji „na
# wszelki wypadek": 293 pozycje AXIS PRO dzielą jedną instrukcję, bo montuje
# się je identycznie. Przypisanie per SKU byłoby 293 kopiami tej samej prawdy.

DOKUMENTY_DIR = os.path.join(os.path.dirname(_HERE), "dokumenty")


@lru_cache(maxsize=1)
def load_dokumenty():
    """Rejestr dokumentów producentów: {id: {...}}. Brak pliku = pusty."""
    path = os.path.join(DATA_DIR, "dokumenty.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sciezka_dokumentu(doc_id):
    """Pełna ścieżka pliku dokumentu. `None`, gdy nie ma go na dysku.

    Rejestr i pliki mogą się rozjechać (ktoś doda wpis, zapomni pliku), więc
    pytanie „czy jest" ma jedną odpowiedź, a nie dwie sprzeczne.
    """
    doc = load_dokumenty().get(doc_id)
    if not doc:
        return None
    sciezka = os.path.join(DOKUMENTY_DIR, doc["plik"].replace("/", os.sep))
    return sciezka if os.path.exists(sciezka) else None


def dokumenty_dla(sku=None, system_id=None, hinge_system_id=None):
    """Dokumenty pasujące do pozycji katalogu albo do systemu.

    Kolejność wyniku jest znacząca: najpierw to, co opisuje DOKŁADNIE tę
    pozycję (dopasowanie po SKU), potem dokumenty całego systemu. Instrukcja
    zawieszki ma być pierwsza, gdy pytamy o zawieszkę, nawet jeśli mebel ma
    też szuflady.
    """
    if sku is not None and system_id is None:
        it = get_item(sku)
        if it:
            system_id = it.get("system_id")

    po_sku, po_systemie = [], []
    for doc in load_dokumenty().values():
        dot = doc.get("dotyczy") or {}
        if sku is not None and sku in (dot.get("sku") or []):
            po_sku.append(doc)
        elif system_id is not None and system_id in (dot.get("systemy") or []):
            po_systemie.append(doc)
        elif (hinge_system_id is not None
              and hinge_system_id in (dot.get("systemy_zawiasow") or [])):
            po_systemie.append(doc)
    return po_sku + po_systemie
