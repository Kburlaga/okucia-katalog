# Graph Report - okucia-katalog  (2026-07-25)

## Corpus Check
- 12 files · ~32,170 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 57 nodes · 81 edges · 7 communities (6 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- compute.py
- app.py
- matching.py
- loader.py
- okucia-katalog
- load_systems
- sync_from_kalkulator.py

## God Nodes (most connected - your core abstractions)
1. `compute_drawer_for_opening()` - 7 edges
2. `get_system()` - 7 edges
3. `okucia-katalog` - 7 edges
4. `load_systems()` - 6 edges
5. `pick_nl()` - 5 edges
6. `compute_drawer_parts()` - 5 edges
7. `load_items()` - 5 edges
8. `resolve_system_id()` - 5 edges
9. `related()` - 4 edges
10. `compute_drawer()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `systems()` --calls--> `load_systems()`  [EXTRACTED]
  app.py → okucia/loader.py
- `system()` --calls--> `get_system()`  [EXTRACTED]
  app.py → okucia/loader.py
- `items()` --calls--> `load_items()`  [EXTRACTED]
  app.py → okucia/loader.py
- `item()` --calls--> `get_item()`  [EXTRACTED]
  app.py → okucia/loader.py
- `related()` --calls--> `match_drawer_accessories()`  [EXTRACTED]
  app.py → okucia/matching.py

## Import Cycles
- None detected.

## Communities (7 total, 1 thin omitted)

### Community 0 - "compute.py"
Cohesion: 0.22
Nodes (13): compute_drawer(), Wymiary formatek szuflady wg wzorów systemu., system(), compute_drawer_for_opening(), compute_drawer_parts(), pick_h_class(), pick_nl(), Logika liczona z systems.json — KANONICZNA (zastąpi rozjechane reguły w cutting (+5 more)

### Community 1 - "app.py"
Cohesion: 0.25
Nodes (7): item(), items(), okucia-service — cienka warstwa HTTP nad pakietem `okucia`.  Serwuje katalog +, Auto-dobrane akcesoria (złączki/szkło) dla kompletu szuflady., related(), load_items(), Lista SKU (dict). Opcjonalny filtr po kategorii i/lub systemie.

### Community 2 - "matching.py"
Cohesion: 0.29
Nodes (6): Any, okucia — wydzielony katalog okuć meblowych (dane + logika), współdzielony.  Kr, match_drawer_accessories(), Auto-dobór towarzyszących okuć dla kompletu szuflady.  Port 1:1 logiki z Kalku, Lista towarzyszących SKU dla danego kompletu szuflady (lub [] gdy brak)., _specs()

### Community 3 - "loader.py"
Cohesion: 0.32
Nodes (7): get_hinge_system_by_name(), get_item(), _load_all_items(), load_hinge_systems(), Ładowanie danych katalogu z folderu data/.  - systems.json — parametry technic, Zwraca dict {hinge_system_id: {...}} z hinge_systems.json., Wyszukuje system zawiasów po polu `name` (np. 'Blum Clip Top'). None gdy brak.

### Community 4 - "okucia-katalog"
Cohesion: 0.25
Nodes (7): Aktualizacja danych, Co tu jest, okucia-katalog, Roadmap do jednego źródła, Serwis HTTP (Faza 2), Użycie (np. ze skryptu Fusion), Znany rozjazd do naprawienia (Faza 3)

### Community 5 - "load_systems"
Cohesion: 0.33
Nodes (7): systems(), get_drawer_system_by_name(), load_systems(), Zwraca dict {system_id: {...parametry...}}., Wyszukuje system szuflad po polu `name` (np. 'GTV Axis Pro'). None gdy brak., Zwraca id systemu szuflad. Przyjmuje gotowe id (np. 'gtv_axis_pro') albo     na, resolve_system_id()

## Knowledge Gaps
- **6 isolated node(s):** `Co tu jest`, `Użycie (np. ze skryptu Fusion)`, `Aktualizacja danych`, `Serwis HTTP (Faza 2)`, `Znany rozjazd do naprawienia (Faza 3)` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `related()` connect `app.py` to `matching.py`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `get_system()` connect `compute.py` to `loader.py`, `load_systems`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `load_items()` connect `app.py` to `loader.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **What connects `Co tu jest`, `Użycie (np. ze skryptu Fusion)`, `Aktualizacja danych` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._