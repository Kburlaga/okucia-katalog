"""
Odświeża data/items/ kopiując seedy SKU z projektu Kalkulator_Stolarski_3.

To utrzymuje „jedno miejsce edycji" w okresie bliźniaka: katalog SKU edytujesz
w kalkulatorze (backend/seed/gtv_*.json), a tu robisz tylko `python tools/sync_from_kalkulator.py`.

Uwaga: systems.json NIE jest nadpisywany (zawiera dane uzupełnione z karty
technicznej, których kalkulator jeszcze nie ma). Synchronizujemy tylko items/.
"""
import glob
import os
import shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
ITEMS_DIR = os.path.join(ROOT, "data", "items")

KALK_SEED = r"d:\Programowanie\Kalkulator_Stolarski_3\backend\seed"


def main():
    os.makedirs(ITEMS_DIR, exist_ok=True)
    seeds = sorted(glob.glob(os.path.join(KALK_SEED, "gtv_*.json")))
    if not seeds:
        raise SystemExit(f"Nie znaleziono seedów w {KALK_SEED!r} — sprawdź ścieżkę.")
    copied = 0
    for src in seeds:
        dst = os.path.join(ITEMS_DIR, os.path.basename(src))
        shutil.copyfile(src, dst)
        copied += 1
        print(f"  {os.path.basename(src)}")
    print(f"Zsynchronizowano {copied} plików -> {ITEMS_DIR}")


if __name__ == "__main__":
    main()
