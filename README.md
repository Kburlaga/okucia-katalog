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
  dokumenty.json  rejestr instrukcji producenta: co opisuje który plik
dokumenty/      SAME instrukcje (PDF), ułożone wg producenta
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
i zdalnych. Read-only, bez logowania (zasób w sieci lokalnej). Port hosta **8015**.

Endpointy:
- `GET /health`
- `GET /systems` , `GET /systems/{id}`
- `GET /items?category=&system_id=` , `GET /items/{sku}` , `GET /items/{sku}/related`
- `GET /compute/drawer?lw=&depth=&system_id=&h_class=&front_h=` (zamiast `depth` można podać `nl`)
- `GET /dokumenty?sku=&system_id=&hinge_system_id=` , `GET /dokumenty/{id}/plik`

Lokalnie: `uvicorn app:app --reload --port 8000`
Serwer: `docker compose up --build -d` (deploy automatyczny przez `.github/workflows/deploy.yml`).

## Dokumenty producentów

Katalog trzymał dotąd WARTOŚCI wyjęte z kart producenta (`specs.source_pdf`,
`specs.source_page`) i nie trzymał samych kart. Liczba bez dokumentu jest nie
do sprawdzenia, a stolarz przy maszynie i tak potrzebuje rysunku montażowego,
a nie tabelki.

**Dokument należy do SYSTEMU albo do SKU, nigdy do pojedynczej pozycji „na
wszelki wypadek".** 293 pozycje AXIS PRO dzielą jedną instrukcję, bo montuje
się je identycznie; przypisanie per SKU byłoby 293 kopiami tej samej prawdy.

`data/dokumenty.json` niesie też `strony` — nazwane numery stron („montaż",
„wymiary montażowe"). Dzięki temu link otwiera kartę NA WŁAŚCIWEJ STRONIE,
a nie na okładce dokumentu, który ma ich siedemdziesiąt cztery.

`specs.source_pdf` zostaje i znaczy co innego: to dowód pochodzenia LICZBY
(z którego pliku i której strony ją przepisano), a nie instrukcja montażu.
Dwie różne rzeczy, dwa różne pola.

Walidator sprawdza obie strony rozjazdu: wpis bez pliku (martwy link
w aplikacji) i plik bez wpisu (nikt go nie zobaczy).

## Walidacja kompletności

Wymagane pola techniczne per kategoria opisuje `okucia/schema.py` — to kod,
nie proza, więc da się to sprawdzić:

```
python tools/validate_catalog.py            # raport zbiorczy
python tools/validate_catalog.py --verbose  # z listą SKU
python tools/validate_catalog.py --strict   # kod wyjścia 1 przy brakach (CI)
```

Sprawdzana jest obecność **i niepustość** — `{"nl_mm": null}` to brak danej,
a nie dana. Gdy pole naprawdę nie dotyczy pozycji (zawias narożny nie ma
zakresu nakładki, uchwyt frezowany nie ma rozstawu otworów), wpisuje się je
w `specs.not_applicable` wraz z `not_applicable_reason` — udokumentowany
wyjątek jest lepszy niż zmyślona liczba wpisana, żeby walidator zamilkł.

Ten sam raport wystawia kalkulator pod `GET /catalog/health`.

**Stan na 2026-07-28:** systemy mają komplet pól, ale 434 z 444 pozycji ma
puste pole wymagane — to pozostałość po parserach PDF-ów GTV (m.in.
`min_carcass_depth_mm`/`min_carcass_width_mm` puste we wszystkich 293
kompletach szuflad, `force_min_N`/`force_max_N` we wszystkich podnośnikach).
Nie blokuje to dzisiejszych obliczeń, bo te idą z `systems.json`, ale blokuje
walidacje typu „czy ten komplet zmieści się w tym korpusie".

## Roadmap do jednego źródła
1. ~~bliźniak + Fusion liczy z tego modułu~~ — zrobione.
2. ~~**Faza 2:** owinąć `okucia` w FastAPI + Docker + runner + port~~ — zrobione
   (`app.py`, port 8015).
3. ~~**Faza 3:** kalkulator przepięty na wspólny moduł, usunięcie duplikatów~~ —
   zrobione 2026-07-28. Kalkulator nie ma już własnych kopii offsetów ani
   redukcji cięcia: `hardware.py` czyta je stąd, `HardwareSystem` w bazie jest
   seedowany z tego katalogu, a `drilling.py` nie zawiera literałów rozstawów.
4. **Do zrobienia:** uzupełnić puste pola wymagane (patrz walidacja wyżej)
   i potwierdzić kartami producentów pozycje z `verified: false` oraz systemy
   z `drilling_verified: false`.
