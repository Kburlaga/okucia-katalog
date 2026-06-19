# okucia-katalog

Wydzielony **katalog okuć meblowych** (dane + logika) — wspólny zasób dla wielu
programów. Krok 1: „bliźniak" dla modelowania w **Autodesk Fusion**; docelowo
**jeden katalog aktualizowany w jednym miejscu**.

## Co tu jest
```
okucia/         czysty Python (tylko stdlib), bez web/DB
  loader.py     wczytywanie systems.json + items/*.json
  compute.py    compute_drawer_parts(LW, NL, system_id, h_class) + pick_nl(...)
  matching.py   match_drawer_accessories(sku, items) — auto-dobór złączek
data/
  systems.json  parametry systemów (redukcje cięcia, offsety, klasy H, NL)
  items/        katalog SKU (kopie z kalkulatora — patrz sync)
tools/
  sync_from_kalkulator.py   odświeża data/items/ z Kalkulator_Stolarski_3
```

## Użycie (np. ze skryptu Fusion)
```python
import sys; sys.path.insert(0, r"d:\Programowanie\okucia-katalog")
from okucia import compute, matching, loader

p = compute.compute_drawer_parts(LW=573, NL=550,
                                 system_id="gtv_axis_pro", h_class="D")
# p["dno"] = {width:498, depth:526, thickness:16}
# p["tyl"] = {width:486, height:199, thickness:16}
# p["bok"] = {thickness:14, height:200, length:550}

acc = matching.match_drawer_accessories("PB-AXISPRO-KPL550D1", loader.load_items())
```

## Aktualizacja danych
- **Katalog SKU** edytuje się w kalkulatorze (`backend/seed/gtv_*.json`), tu:
  `python tools/sync_from_kalkulator.py` (kopiuje do `data/items/`).
- **systems.json** trzymany tutaj — zawiera dane z karty technicznej GTV,
  których kalkulator jeszcze nie ma (min. wysokości korpusu per klasa,
  grubość boku 14 mm, próg relingu 284 mm).

## Serwis HTTP (Faza 2)
Cienka warstwa REST nad pakietem (`app.py`, FastAPI) — dla programów nie-Pythonowych
i zdalnych. Read-only, bez logowania (zasób w sieci lokalnej). Port hosta **8014**.

Endpointy:
- `GET /health`
- `GET /systems` , `GET /systems/{id}`
- `GET /items?category=&system_id=` , `GET /items/{sku}` , `GET /items/{sku}/related`
- `GET /compute/drawer?lw=&depth=&system_id=&h_class=&front_h=` (zamiast `depth` można podać `nl`)

Lokalnie: `uvicorn app:app --reload --port 8000`
Serwer: `docker compose up --build -d` (deploy automatyczny przez `.github/workflows/deploy.yml`).

## Znany rozjazd do naprawienia (Faza 3)
W kalkulatorze logika szuflady jest w 3 miejscach i się różni:
- `HardwareSystem` (tabela): dno `LW−75`, tył `LW−87` — POPRAWNE, tego używa ten moduł.
- `cutting_list_v3.py`: dno liczone `LW−87` (błąd), NL zgadywane.
- `hardware.py` (`DRAWER_SYSTEMS`): trzecia kopia offsetów.

## Roadmap do jednego źródła
1. **(ten krok)** bliźniak + Fusion liczy z tego modułu.
2. **Faza 2:** owinąć `okucia` w FastAPI + Docker + runner + port → dostęp HTTP
   dla programów nie-Pythonowych. Reużywa tego samego jądra.
3. **Faza 3:** kalkulator stolarski przepięty na wspólny moduł/serwis,
   usunięcie duplikatów i rozjazdu (ostrożnie, na gałęzi, z testami).
