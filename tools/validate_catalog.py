"""Sprawdza kompletność katalogu wobec kontraktu z okucia/schema.py.

    python tools/validate_catalog.py          # raport
    python tools/validate_catalog.py --strict # kod wyjścia 1 przy brakach (CI)

Braki twarde (brakujące/puste pola wymagane) to błąd. Pozycje `verified: false`
i systemy bez pól opcjonalnych są tylko wypisywane — to stan do nadrobienia,
a nie powód, żeby blokować budowanie.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from okucia import schema  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="zwróć 1, gdy są braki wymaganych pól")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="wypisz każde SKU osobno zamiast zbiorczo")
    args = ap.parse_args()

    r = schema.validate_catalog()
    from okucia import loader
    cat_by_sku = {it.get("sku"): it.get("category") for it in loader.load_items()}

    print(f"Pozycji w katalogu: {r['items_total']}")

    if r["systems_with_problems"]:
        print(f"\nSYSTEMY Z BRAKAMI ({len(r['systems_with_problems'])}):")
        for sid, problems in sorted(r["systems_with_problems"].items()):
            print(f"  {sid}")
            for p in problems:
                print(f"      {p}")

    if r["items_with_problems"]:
        n_items = len(r["items_with_problems"])
        print(f"\nPOZYCJE Z BRAKAMI ({n_items}):")
        if args.verbose:
            for sku, problems in sorted(r["items_with_problems"].items()):
                print(f"  {sku}")
                for p in problems:
                    print(f"      {p}")
        else:
            # Zbiorczo: braki idą całymi kategoriami (parser PDF-ów zostawiał
            # to samo pole puste w setkach pozycji naraz), więc lista SKU po
            # jednym na wiersz nic nie mówi, a zasłania obraz.
            from collections import Counter
            agg = Counter()
            for sku, problems in r["items_with_problems"].items():
                for p in problems:
                    agg[(cat_by_sku.get(sku, "?"), p)] += 1
            for (cat, p), n in sorted(agg.items(), key=lambda kv: -kv[1]):
                print(f"  {n:5d}x  {cat:16s} {p}")
            print("\n  (--verbose pokaże pojedyncze SKU)")

    if r["degraded_systems"]:
        print("\nSYSTEMY DZIAŁAJĄCE W TRYBIE OGRANICZONYM:")
        for sid, missing in sorted(r["degraded_systems"].items()):
            print(f"  {sid}")
            for field, why in missing.items():
                print(f"      brak `{field}` — {why}")

    if r["unverified"]:
        print(f"\nNIEZWERYFIKOWANE Z KARTAMI PRODUCENTA ({len(r['unverified'])}):")
        print("  " + ", ".join(r["unverified"]))

    if r["ok"]:
        print("\nOK: wszystkie pozycje i systemy mają komplet pól wymaganych.")
    else:
        n = len(r["items_with_problems"]) + len(r["systems_with_problems"])
        print(f"\nBRAKI: {n} wpisów wymaga uzupełnienia.")

    return 1 if (args.strict and not r["ok"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
