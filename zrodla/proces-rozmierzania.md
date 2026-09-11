# Proces rozmierzania szuflad — synteza

Powstało z trzech materiałów: filmu montażowego Rejs Comfort Box
([rejs-comfort-box.md](rejs-comfort-box.md)), oferty szablonu 3dek do prowadnic
GTV ([gtv-szablon-prowadnic-oferta.md](gtv-szablon-prowadnic-oferta.md)) oraz
z kodu `Kalkulator_Stolarski_3`. Każde twierdzenie o zachowaniu aplikacji ma
tu wskazane miejsce w kodzie — nic nie jest z pamięci.

**Status: notatka źródłowa.** Nie zmienia ani katalogu, ani kodu.

## Dwa niezmienniki, których nie wolno pomylić

**1. Oś prowadnicy → nawiert mocowania frontu jest STAŁA.** To czysty sprzęt:
`base_front_y − offset_prowadnica`. Dla GTV Axis Pro 47,5 − 32 = **15,5 mm**.
Nie zależy od żadnego ustawienia projektu — gdyby zależała, front nie trafiłby
w zaczep na skrzynce. Pilnuje tego
`backend/tests/test_pelne_milimetry.py::test_mocowanie_lezy_nad_osia_prowadnicy_o_stala_katalogowa`.

To ta stała sprawia, że szablon do prowadnic i szablon do frontów mogą być
sprzedawane jako komplet: jeden wyznacza oś, drugi nawiert, a odległość między
nimi jest z góry ustalona przez okucie.

**2. Dolna krawędź frontu → oś prowadnicy NIE jest stała.** To wielkość pochodna
i zmienia się z wariantem stosu oraz z tym, czy to szuflada dolna. Mylenie jej
z niezmiennikiem nr 1 jest najłatwiejszym błędem w całym rozmierzaniu.

Kod trzyma to w `module_geometry.py` jako osobne pole każdego frontu:

```python
"ov_d_frontu": ov_d + (yp - y_rel),
# Przelicznik z dna światła na dolną krawędź TEGO frontu.
# Nawiert mocowania musi trafić w zaczep skrzynki, więc idzie
# za osią, a nie za nałożeniem dolnym mebla.
```

## Dwa punkty odniesienia

Pod najniższą szufladą jest dolny wieniec i tylko od niego da się mierzyć.
Pod pozostałymi nie ma nic — zostaje dolna krawędź frontu. Dlatego **najniższa
prowadnica ma inny punkt bazowy niż wszystkie powyżej**, i to nie jest konwencja,
tylko konieczność.

Widać to w obu materiałach niezależnie: szablon 3dek przykłada się najpierw do
wieńca, potem do trasowanej linii frontu; autor filmu odmierza 55 mm od spodu
korpusu dla pierwszej prowadnicy i 72 mm od dołu frontu dla drugiej.

W kodzie to `_osie_prowadnic` (`module_geometry.py`), gdzie szuflada `i == 0`
jest traktowana osobno.

## Przebieg

### 1. Wymiary zewnętrzne → światło i głębokość efektywna
Z szerokości zewnętrznej robi się **LW** (światło korpusu) — z niego liczą się
wszystkie formatki skrzynki. Z głębokości robi się głębokość dostępna pod
prowadnicę; **push-to-open zabiera z niej zapas** (`ZAPAS_PUSH_TO_OPEN_MM`),
bo front musi mieć gdzie się cofnąć przy naciśnięciu.

### 2. Liczba szuflad i wysokości frontów
Klasy wysokości jeszcze NIE — to wynik, nie dana wejściowa (patrz krok 7).

### 3. Szpary, nałożenia, typ frontu
Nałożenie dolne `ov_d`, górne `ov_g`, odstęp między frontami, oraz czy front jest
**nakładany czy wpuszczany**. Front wpuszczany nie ma nałożenia, więc kroki 5 i 6
zlewają się w jeden — oba warianty dają wtedy to samo.

### 4. Podział wysokości na fronty i szpary
`_rozmierz_fronty`. Przy najwyższym module w stosie nałożenie górne może zostać
skorygowane (zwracane jako `nowa_ov_g`).

### 5. Wybór wariantu stosu — KROK NAJCZĘŚCIEJ POMIJANY
`ModuleDetails.szuflady_wymienne`:

| | Co robi | Cena |
|---|---|---|
| `True` (domyślnie) | „fejkowe nałożenie" — nałożenie dolne dokłada się do KAŻDEJ szuflady | każda powyżej dolnej traci `ov_d` mm światła |
| `False` | szuflady od drugiej w górę schodzą o `ov_d` | koniec wymienności skrzynek **i frontów** |

W wariancie `False` **front dolny wierci się inaczej niż pozostałe** — o całe
nałożenie dolne. To jest sedno nazwy „wymienne".

Wariant `False` odpowiada temu, jak liczy szablon GTV PB-SZABLON-AXIS-MB
(serie 47 · +126 · +144 · +144 · +144 — pierwszy krok krótszy dokładnie
o nałożenie). Autor filmu o Comfort Boxie wybiera świadomie wariant `True`,
mówiąc wprost, że chce móc zamienić szuflady miejscami.

Aplikacja nie rozstrzyga tego za użytkownika i podaje koszt wyboru w milimetrach:
`uwagi.py::_zysk_z_obnizenia`.

### 6. Osie prowadnic ze stosu frontów
`_osie_prowadnic(y_fronty, ov_d, front_inset, wymienne)`. Dolna osobno, reszta
wedle wariantu z kroku 5.

### 7. Dobór klasy wysokości — TU UKŁAD MOŻE ZOSTAĆ ODRZUCONY
Klasa musi spełnić **dwa warunki naraz**, a `pick_h_class` przyjmuje jedną liczbę,
więc `_swiatlo_na_klase` podaje mniejszy z nich:

1. **Skrzynka mieści się w świetle.** Szuflada pośrednia sięga do osi sąsiadki
   wyżej (`krok`), najwyższa do górnego wieńca.
2. **Mocowania wypadają na froncie.** Punkty z `mocowania_frontu` liczą się od
   krawędzi frontu i rosną razem z klasą — niski front nie uniesie wysokiej
   skrzynki niezależnie od tego, ile jest światła.

Do 2026-09-03 aplikacja znała tylko warunek 2: szafka 600×820 z trzema szufladami
GTV Axis Pro dobierała górnej klasę D (wymaga 198 mm nad osią) tam, gdzie światła
było 176.

### 8. Nawierty mocowania frontu
Z osi prowadnicy, przez stałą z niezmiennika nr 1, **per front** — z użyciem
`ov_d_frontu` tego frontu, nie nałożenia dolnego mebla.

### 9. Dobór NL i rozkrój
Z głębokości efektywnej. NL decyduje o dwóch rzeczach naraz:

- **który otwór prowadnicy wiercisz** (`slide_screw_spacing_by_nl`),
- **jak tniesz dno i tył.**

| System | Dno szer. | Dno gł. | Tył szer. |
|---|---|---|---|
| GTV Axis Pro (płyta 16) | `LW − 75` | `NL − 24` | `LW − 87` |
| Rejs Comfort Box | `LW − 35` | `NL − 7` | `LW − 89` |

## Kierunek przyczynowości

W warsztacie: wiercisz prowadnice, a front ląduje tam, gdzie one każą.
W rachunku: najpierw dzielisz wysokość na fronty, potem z nich wychodzą osie
(`_osie_prowadnic` przyjmuje `y_fronty` i zwraca `y_prow`).

Oba opisy są poprawne, bo sprzężenie jest sztywne w obie strony — ale są to dwa
różne opisy i nie należy ich mieszać w jednej liście kroków.

## Otwarte, z tych materiałów

- **`offset_prowadnica` 32 (Axis Pro) vs 33 (Modern Box).** Skoro `base_front_y`
  jest identyczne (47,5), a jedna para szablonów ma obsługiwać oba systemy, to
  stała z niezmiennika nr 1 musiałaby być wspólna. Jest 15,5 i 14,5. Jeden wpis
  jest zły; podejrzanym jest 33, bo Modern Box ma `drilling_verified: false`.
- **Otwór „+32 mm" od pierwszego** — szablon 3dek każe go wiercić dla każdego NL,
  katalog i `drilling.py` go nie znają.
- **Mapowanie NL → rozstaw przy Modern Box.** Szablon wskazuje 128/160 dla
  NL 300/350, karta GTV 450454 s.6 mówi 192.
- **Klasy C i D w `gtv_modern_box_pro` są zamienione miejscami** (C = 199,
  D = 167, odwrotnie niż w Axis Pro i Blum Antaro). Znalezione przy okazji,
  niezwiązane z tymi materiałami.
