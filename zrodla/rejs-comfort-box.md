# Rejs Comfort Box — wyciąg z materiału wideo

**Status: materiał źródłowy, NIE wpisany do `data/systems.json`.**
Transkrypt filmu montażowego (język polski, ASR). Pokrywa 7 z 25 pól, których
wymaga schemat systemu szuflad — brakujące wymieniono na końcu. Do pełnego wpisu
potrzebna jest karta katalogowa Rejsa.

## Formuły wymiarowe (z instrukcji dołączonej do zestawu)

Oznaczenia: **LW** = światło korpusu (odległość między bokami), **NL** = długość
nominalna prowadnicy.

| Element | Formuła |
|---|---|
| Szerokość ścianki tylnej | `LW − 89` |
| Wysokość ścianki tylnej | 78 / 124 / 148 / 188 mm (wg tabeli, do wyboru) |
| Szerokość dna | `LW − 35` |
| Długość dna | `NL − 7` |

Przykład podany w materiale: prowadnica NL 500 → dno o długości **493 mm**.
To jedyny wymiar NL, który w materiale pada.

## Montaż prowadnicy

- Pierwsze wkręty w **3. otworze, 37 mm od przodu** korpusu.
- Od spodu prowadnicy do środka otworu montażowego: **ok. 53 mm**.
- Wkręty: w transkrypcie „3/16" — najpewniej **3,5 × 16 mm**, do potwierdzenia.
- Autor daje **4 wkręty na prowadnicę**.
- Prowadnice pod **płytę 16 mm**.

## Praktyka warsztatowa autora (NIE instrukcja producenta)

Rozdzielone świadomie — te liczby to jego konwencja, nie wymóg systemu:

- **Dno tnie na `NL − 5`**, nie `NL − 7`. Sam mówi w materiale: „róbcie tak jak
  w instrukcji".
- Prowadnicę montuje **55 mm od spodu korpusu**, nie 53.
- Front sąsiedniej szafki uchylnej: **713 mm**, montowany **2 mm od spodu korpusu**,
  co zostawia **5 mm** luzu u góry. Wymiar zostawiony „z dawnych czasów", nie wynika
  z systemu.
- Fronty szuflad w pokazywanej szafce: dwie po **284 mm** i trzeci niższy na górze,
  **3 mm luzu** między frontami.
- Dla drugiej szuflady odmierza oś prowadnicy **72 mm od dołu jej frontu** (teoria
  daje 71 mm; różnicę tłumaczy możliwym przesunięciem dolnego wieńca).
- Trzecia, niska szuflada: **60 mm** zamiast 55, żeby zejść niżej pod blat.
- Na co dzień używa szablonu zamiast odmierzania — pokaz „na piechotę" jest po to,
  żeby dało się taki szablon zrobić.

## Montaż i obsługa

- Zawartość pudełka: 2 boczki, 2 prowadnice, mocowania frontu, 2 zaślepki, wkręty
  do mocowań frontu, instrukcja z tabelą wymiarów.
- Ścianka tylna **wsuwana od góry**, zatrzaskuje się na zapadkę. Demontaż: odgiąć
  zapadkę i podważyć.
- Szuflada wpina się na prowadnice; na końcu prowadnicy plastikowy zaczep, trzeba
  docisnąć do wskoczenia. **Z założonym frontem nie zawsze wskakuje do końca** —
  sprawdzić palcem.
- Demontaż szuflady: szarpnięcie do góry.
- Przy szerszych szufladach warto dodatkowo skręcić dno **konfirmatami od spodu**;
  przy wąskich zbędne.
- Relingi okrągłe i prostokątne do wyboru, dostępne też boki szklane (boxside).
- Po zamknięciu szuflada jest **lekko cofnięta względem czoła korpusu** — tak ma być.
- Cichy domyk w standardzie.

## Opinia autora

Jakościowo blisko Blum Tandembox, wyglądem „w zasadzie nie różnią się", istotnie
tańsze. Montuje je od kilku lat bez reklamacji.

## Czego brakuje do wpisu w `data/systems.json`

Schemat wymaga 25 pól wspólnych dla wszystkich systemów. Transkrypt daje:

- `cut_back_width_reduction: 89`
- `cut_bottom_width_reduction: 35`
- `cut_bottom_depth_reduction: 7`
- `h_classes` — cztery wysokości nominalne 78 / 124 / 148 / 188 (bez `real_mm`
  i bez `min_carcass_height_mm`)
- `slide_screw_x_front_mm: 37`
- `base_front_y` — ok. 53
- `available_nl_mm` — wyłącznie 500

Brakuje: `side_thickness_mm`, `offset_prowadnica`, `front_fix_offset_internal`,
`fix_x_internal`, `rail_required_above_front_mm`, `front_fix_second_hole_dy_mm`,
`front_fix_second_hole_min_h_mm`, `slide_screw_spacing_mm`,
`carcass_dowel_x_offset_mm`, `shelf_pin_x_offset_mm`, pełnej listy `available_nl_mm`
oraz `real_mm` / `min_carcass_height_mm` dla klas wysokości.

## Ostrzeżenie o jakości transkryptu

Zapis pochodzi z automatycznego rozpoznawania mowy i **część liczb jest przekręcona**.
Zweryfikowane jako spójne: 89, 35, 7, 493, 500, 78/124/148/188, 37, 53, 55, 16, 713,
284, 2, 3, 5, 72, 60, 18. Uszkodzone i nie do odzyskania z tego materiału:
zapisane przez autora położenia trzech prowadnic mierzone od dołu („74 361",
„66636", „6073") — przy przenoszeniu na drugi bok korpusu podaje je jako gotowe
liczby, których transkrypt nie oddaje. Jednostki „37 metrów" i „7 metrów" to
oczywiście milimetry.
