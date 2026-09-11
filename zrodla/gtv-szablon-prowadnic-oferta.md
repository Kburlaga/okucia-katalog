# Szablon do montażu prowadnic GTV Axis Pro + Modern Box — wyciąg z oferty

**Status: materiał źródłowy, NIE wpisany do `data/systems.json`.**
Tekst ofertowy produktu (szablon drukowany 3D). Wartość informacyjna niska —
**nie podaje ani jednego wymiaru**. Zawiera natomiast metodę pracy i jedną tezę
konstrukcyjną, którą dało się skonfrontować z katalogiem.

## Co wnosi: DWA punkty odniesienia, nie jeden

1. Pierwszą prowadnicę bazuje się o **dolny wieniec szafki**.
2. Dla każdej kolejnej: zaznaczyć **dolną krawędź frontu**, dosunąć boczny
   element szablonu do tej linii, wywiercić otwory.

To jest sedno materiału: **najniższa szuflada ma inny punkt odniesienia niż te
powyżej**. I tak być musi, bo pod najniższą jest wieniec, a pod pozostałymi nie
ma nic, od czego dałoby się mierzyć — zostaje krawędź frontu.

Film o Comfort Boxie robi identycznie: pierwsza prowadnica 55 mm od spodu
korpusu, druga 72 mm od dołu SWOJEGO frontu
(zob. [rejs-comfort-box.md](rejs-comfort-box.md)).

## Jak to siedzi w kalkulatorze

Aplikacja modeluje to rozróżnienie i wystawia je jako wybór użytkownika —
`ModuleDetails.szuflady_wymienne` (`models.py`), obsłużony w `_osie_prowadnic`
(`module_geometry.py`), gdzie szuflada `i == 0` jest traktowana osobno od reszty:

| | `szuflady_wymienne` | Co robi | Koszt |
|---|---|---|---|
| **Domyślnie** | `True` | „fejkowe nałożenie" — do KAŻDEJ szuflady dokłada się nałożenie dolne, więc odległość front→prowadnica jest wszędzie ta sama | każda szuflada powyżej dolnej traci `ov_d` mm światła |
| | `False` | szuflady od drugiej w górę schodzą o `ov_d`, prowadnica siada tuż za szczeliną frontu | skrzynki przestają być wymienne między pozycjami |

Komentarz w `models.py` przypisuje wariant `False` wprost szablonowi
**GTV PB-SZABLON-AXIS-MB** (serie 47 · +126 · +144 · +144 · +144 — pierwszy krok
krótszy dokładnie o nałożenie dolne). Oferowany tu szablon opisuje tę samą
procedurę, więc najpewniej należy do tej samej rodziny, ale oferta nie podaje
serii wymiarowej, więc to wniosek, nie fakt.

**Dwa materiały stoją po przeciwnych stronach tego przełącznika:**
autor filmu o Comfort Boxie świadomie wybiera wariant wymienny — mówi wprost,
że chce móc zamienić obie szuflady miejscami i że te „dwa centymetry go nie
zbawią". Szablon GTV liczy tak, jak wariant `False`.

Aplikacja niczego tu nie rozstrzyga za użytkownika i podpowiada cenę wyboru:
`uwagi.py::_zysk_z_obnizenia` wypisuje, ile milimetrów wróci górnej szufladzie
po wyłączeniu wymienności.

Nic z tego nie wymaga zmiany w kodzie — metoda z oferty jest już zaimplementowana.

## Teza do rozstrzygnięcia: jeden szablon na oba systemy

Oferta twierdzi, że ten sam szablon obsługuje **Axis Pro i Modern Box**, co
znaczy, że oba mają identyczną geometrię otworów prowadnicy. Katalog mówi
częściowo co innego:

| Pole | Axis Pro | Modern Box Pro | |
|---|---|---|---|
| `slide_screw_x_front_mm` | 37,0 | 37,0 | zgodne |
| `slide_screw_spacing_mm` | 224,0 | 224,0 | zgodne |
| `base_front_y` | 47,5 | 47,5 | zgodne |
| `fix_x_internal` | 15,5 | 15,5 | zgodne |
| `offset_prowadnica` | 32,0 | **33,0** | różnica 1 mm |
| `slide_screw_second_row_mm` | 44,0 | **49,0** | różnica 5 mm |

Geometria pozioma i mocowanie frontu są identyczne — na tyle szablon ma sens.
Rozjeżdża się **pion**: odsuw osi prowadnicy od dna światła różni się o 1 mm,
a drugi rząd wkrętów o 5 mm.

Trzy możliwe wyjaśnienia, żadnego nie da się rozstrzygnąć z tej oferty:
- szablon ma osobne oznaczenia dla obu systemów (oferta o tym nie mówi),
- 1 mm mieści się w regulacji prowadnicy i producent szablonu to ignoruje,
- **wartość w katalogu dla Modern Box jest błędna** — ten system ma
  `drilling_verified: false`, podczas gdy Axis Pro jest potwierdzony kartami
  (CZ 5 str. + PL 2 str., 2026-08-31).

Do rozstrzygnięcia przymiarem albo kartą Modern Box PRO (PDF 450454, s.6).

## Reszta treści oferty

- Otwory nawierca się **wiertłem Ø3 mm**; szablon ma stalowe tuleje Ø3.
- Materiał PETG, odporność do 70 °C.
- Zalecane ściski stolarskie.
- Istnieje osobny, komplementarny szablon do montażu frontów.

Nic z tego nie jest daną wymiarową systemu i nie ma miejsca w `systems.json`.

---

# Odczyt ze zdjęć produktu (2026-09-08)

Źródło: https://3dek.pl/szablon-do-montazu-prowadnic-szuflad-gtv-axis-pro-modern-box
Zdjęcia to rendery 3D samego szablonu, z naniesionymi wymiarami. **Opis oferty
nie podaje żadnej liczby poza Ø3 mm — wszystkie poniższe pochodzą z grafiki.**

## Jak szablon działa

Listwa kładziona **poziomo** na boku korpusu: długą krawędzią na linii bazowej,
końcem licując z czołem boku. Obie długie krawędzie są opisane identycznie —
„Dolna linia frontu | Dolny wieniec" — czyli listwa jest symetryczna i działa
w obie strony. Linia otworów biegnie w głąb szafki.

## Zmierzone pozycje otworów

Siedem tulei na **jednej linii**. Skala odczytana z pikseli renderu w rozdzielczości
1280 px: 104,1 px na 32 mm, powtarzalne w granicach 0,5 px na wszystkich odstępach.

| Odsuw od otworu „0" | Opis na szablonie | Odległość od czoła boku |
|---|---|---|
| 0 | NL Wszystkie | 37 mm |
| 32 | NL Wszystkie | 69 mm |
| 96 | NL 250 | 133 mm |
| 128 | NL 250 · 300 · 350 | 165 mm |
| 160 | NL 300 · 350 | 197 mm |
| 192 | NL 400 | 229 mm |
| 224 | NL 450 do 600 | 261 mm |

Wymiar „37" jest naniesiony jako odsuw otworu „0" od końca listwy — zgadza się
co do milimetra z `slide_screw_x_front_mm` w katalogu dla obu systemów.

## Konfrontacja z katalogiem

### 1. Otwór „+32 mm" nie istnieje w katalogu

Szablon każe wiercić DWA otwory przy czole, dla każdej długości prowadnicy:
37 i 69 mm. Katalog zna tylko `slide_screw_x_front_mm: 37`, a `drilling.py`
rysuje pierwszy otwór plus rozstawy z `slide_screw_spacing_by_nl` — otworu +32
nie ma skąd wziąć. Dla NL 500 szablon daje trzy otwory (37 · 69 · 261),
aplikacja dwa (37 · 261).

Do sprawdzenia kartą GTV (AXIS PRO CZ s.2). Uwaga: `drilling_source` Axis Pro
wspomina „wymiar 44 i 37,5", więc karta może opisywać tę okolicę inaczej.

### 2. Mapowanie NL → rozstaw zgadza się z Axis Pro, NIE z Modern Box

| NL | Szablon | Katalog Axis Pro | Katalog Modern Box |
|---|---|---|---|
| 250 | 96 · 128 | 96 | — (brak NL 250) |
| 300 | 128 · 160 | 128 | **192** |
| 350 | 128 · 160 | 128 | **192** |
| 400 | 192 | 192 | 192 |
| 450–550 | 224 | 224 | 224 |
| 600 | 224 | 224 · 352 | — |

Pierwsza pozycja z pary szablonu zgadza się z Axis Pro **dla każdego NL**.
Modern Box rozjeżdża się o 64 mm przy NL 300 i 350 — a jego wartość 192 pochodzi
wprost z tabeli producenta (instrukcja 450454 s.6, „WYMIARY MONTAŻOWE DLA
PROWADNIC"), więc to nie jest luźne oszacowanie.

**Wniosek:** szablon jest w istocie szablonem AXIS PRO, sprzedawanym jako wspólny
dla obu systemów. Przy Modern Box NL 300/350 jego otwory nie trafią tam, gdzie
każe karta GTV. Do rozstrzygnięcia przymiarem — ale przy Modern Box nie należy
mu ufać w ciemno.

## Powiązanie osi prowadnicy z mocowaniem frontu

Skoro sprzedawca oferuje osobny szablon do frontów i deklaruje, że oba współpracują,
to odległość między osią prowadnicy a nawiertem mocowania frontu musi być stała.
**Aplikacja już to zakłada i pilnuje testem** —
`test_pelne_milimetry.py::test_mocowanie_lezy_nad_osia_prowadnicy_o_stala_katalogowa`:

> „Odległość nawiertu od osi to czysty sprzęt: `base_front_y` minus
> `offset_prowadnica`. Nie zależy od żadnego ustawienia projektu — gdyby
> zależała, front nie trafiłby w zaczep na skrzynce."

Ta stała wynosi:

| System | `base_front_y` | `offset_prowadnica` | różnica |
|---|---|---|---|
| GTV Axis Pro | 47,5 | 32,0 | **15,5** |
| GTV Modern Box Pro | 47,5 | 33,0 | **14,5** |

I tu wychodzi sedno: **jeżeli ta sama para szablonów obsługuje oba systemy, ta
stała musi być dla obu identyczna.** `base_front_y` jest identyczne (47,5), więc
cała rozbieżność siedzi w `offset_prowadnica`. Jeden z tych dwóch wpisów jest zły.

Axis Pro ma `drilling_verified: true` i dwie karty producenta za sobą.
Modern Box ma `drilling_verified: false`. **Podejrzanym jest 33 przy Modern Box** —
ale to wniosek z logiki szablonu, nie odczyt z karty. Potwierdzić kartą 450454.
