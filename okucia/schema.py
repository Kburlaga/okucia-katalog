"""Wymagane pola techniczne per kategoria — kontrakt katalogu.

Dotąd ta wiedza istniała wyłącznie jako proza w CLAUDE.md kalkulatora
(sekcja „Słownik kategorii okuć i akcesoriów"). Nic jej nie egzekwowało:
pozycja dorzucona bez wymaganego pola przechodziła import bez słowa i wysypywała
się dopiero przy pierwszym użyciu — albo wcale, gdy pole trafiało w `.get()`
z wartością domyślną. Ten moduł zamienia tamtą listę w kod.

Sprawdzamy obecność ORAZ niepustość: `{"min_overlay_mm": null}` to brak danej,
a nie dana. Klucz istniał, więc samo `in specs` by tego nie złapało.

Gdy pole naprawdę nie ma sensu dla danej pozycji (zawias narożny nie ma zakresu
nakładki), wpisuje się je jawnie w `specs.not_applicable` — lepiej mieć
udokumentowany wyjątek niż zmyśloną liczbę wpisaną, żeby walidator zamilkł.
"""

# Pola techniczne, bez których aplikacja nie policzy pozycji poprawnie.
# Źródło: Kalkulator_Stolarski_3/CLAUDE.md, oznaczenia (R).
REQUIRED_FIELDS = {
    "drawer_set": (
        "nl_mm", "h_drawer_class", "h_drawer_mm", "min_carcass_depth_mm",
        "min_carcass_width_mm", "opening_type", "load_capacity_kg",
        "extension_type", "kind",
    ),
    "drawer_slide": ("length_mm", "extension_type", "load_capacity_kg", "mounting_type"),
    "hinge": (
        "angle_deg", "cup_diameter_mm", "cup_depth_mm", "puszka_offset_mm",
        "screw_holes_pitch_mm", "overlay_type", "min_overlay_mm", "max_overlay_mm",
        "min_door_thickness_mm", "max_door_thickness_mm", "soft_close",
    ),
    "handle": (
        "length_mm", "hole_pitch_mm", "width_mm", "height_mm", "protrusion_mm",
        "mounting_screw_thread", "mounting_type",
    ),
    "knob": ("diameter_mm", "height_mm", "protrusion_mm", "mounting_thread"),
    "led_lighting": ("length_mm", "voltage_v", "power_w", "color_temp_k", "mounting_type"),
    "kitchen_accessory": (
        "accessory_type", "fits_carcass_width_mm", "depth_mm", "height_mm",
        "compatible_drawer_systems", "min_drawer_h_class",
    ),
    "connector": (
        "mount_position", "compatible_h_class", "h_value_mm",
        "compatible_systems", "units_per_pack",
    ),
    "mount": ("mount_type", "compatible_systems", "units_per_pack"),
    "rail": (
        "length_mm", "cross_section", "diameter_or_side_mm",
        "compatible_systems", "compatible_h_class",
    ),
    "glass_panel": (
        "length_mm", "height_mm", "thickness_mm",
        "compatible_h_class", "compatible_systems",
    ),
    "cargo": (
        "accessory_type", "fits_carcass_width_mm", "min_carcass_depth_mm",
        "min_carcass_height_mm", "mounting_type", "compatible_drawer_systems",
        "load_capacity_kg", "extension_type",
    ),
    "lift_mechanism": (
        "lift_type", "force_min_N", "force_max_N", "min_door_weight_kg",
        "max_door_weight_kg", "min_door_height_mm", "max_door_height_mm",
        "min_door_width_mm", "max_door_width_mm", "opening_angle_deg",
        "mounting_position", "soft_close",
    ),
    "handleless_system": (
        "system_family", "component_type", "cross_section_mm",
        "compatible_carcass_thickness_mm", "compatible_front_thickness_mm",
    ),
    "drawer_insert": (
        "insert_type", "fits_drawer_width_mm", "fits_drawer_depth_mm",
        "compatible_drawer_systems", "compatible_h_class",
        "width_mm", "depth_mm", "height_mm", "material",
    ),
    "legs": (
        "length_mm", "adjustment_range_mm", "load_capacity_kg",
        "mounting_type", "mounting_thread", "count_per_furniture",
    ),
    # Kategorie spoza słownika w CLAUDE.md — dopisane wraz z pozycjami drążków.
    "wardrobe_rod": (
        "profile", "width_mm", "height_mm", "offset_from_back_mm",
        "cut_clearance_mm", "supports_per_rod", "support_sku", "unit",
    ),
    "wardrobe_rod_support": ("fits_profile", "pieces_per_set", "unit"),
    # Zawieszka mebla wiszącego. Montuje się ją WEWNĄTRZ korpusu, w górnym
    # tylnym narożniku boku, więc jej offsety są danymi wiertarskimi tak samo
    # jak puszka zawiasu — bez nich kalkulator umiałby ją tylko wycenić.
    #
    # `count_per_furniture` liczy SZTUKI (2: lewa + prawa), a `pieces_per_set`
    # mówi, po ile sztuk sprzedaje je producent. Liczba opakowań to iloraz —
    # trzymanie tego w jednej liczbie myliło zamówienie z montażem.
    # Zakres regulacji NIE jest polem wymaganym: nic z niego nie liczymy, idzie
    # tylko do podpowiedzi w instrukcji. Karta R1 go nie podaje, a karta R0 mowi
    # "z regulacja" bez liczby - wymaganie go zablokowaloby obie pozycje przez
    # dana, ktora nie wplywa na zaden wymiar.
    "hanging_bracket": (
        "load_capacity_kg", "pieces_per_set", "count_per_furniture", "unit",
        "mount_offset_top_mm", "mount_offset_back_mm",
        "screw_hole_pitch_mm", "screw_hole_count", "screw_diameter_mm",
        "requires_back_cutout",
        # Wyciecie w plecach i polozenie szyny. Bez nich zawieszka jest
        # policzona i narysowana na boku, ale nie da sie powiedziec, gdzie
        # przykrecic szyne do sciany ani czego wyciac w HDF.
        "back_cutout_width_mm", "back_cutout_height_mm",
        "rail_top_from_carcase_top_mm", "rail_sku",
        # Obrys korpusu zawieszki. Zawieszka jest DOSUNIETA do tylnej krawedzi
        # boku i do gory - offsety wkretow musza wypasc w obrebie tego obrysu.
        # Same offsety bez obrysu pozwalaly wpisac wartosc, przy ktorej wkret
        # wypada obok zawieszki i nikt tego nie widzi.
        "body_width_mm", "body_height_mm",
        # Pozycje wkretow wzgledem GORNEGO TYLNEGO naroznika boku, jako lista
        # par [od tylu, od gory]. Wczesniej byl tylko `mount_offset_*` plus
        # rozstaw, co zakladalo, ze wkrety stoja jeden POD drugim - a karty GTV
        # R0/R1 pokazuja dwa wkrety OBOK siebie, rozstawione w glab boku.
        "screw_holes",
    ),
    # Szyna montazowa, na ktorej wiszą zawieszki. Wyceniana na metry biezace,
    # bo tnie sie ja na szerokosc mebla (albo ciagiem pod kilka szafek).
    "hanging_rail": (
        "profile_height_mm", "profile_thickness_mm", "unit",
        "screw_spacing_mm", "screw_diameter_mm", "wall_hole_diameter_mm",
        "cut_clearance_mm",
    ),
    # Złączka korpusu: konfirmat, mimośród albo wkręt samowiercący. Wybór
    # zmienia i wiercenia, i listę zakupów, więc wymiary muszą być danymi
    # katalogu, a nie stałymi w kodzie rysunków.
    #
    # Pola nieistotne dla danego typu (konfirmat nie ma bębenka) wpisuje się
    # w `specs.not_applicable` — inaczej trzeba by wymyślać dla nich liczby.
    "carcass_fastener": (
        "fastener_type", "unit", "length_mm",
        "face_hole_diameter_mm", "edge_hole_diameter_mm", "edge_hole_depth_mm",
        "cam_diameter_mm", "cam_depth_mm", "cam_axis_from_edge_mm",
        "uses_dowels", "dowel_sku",
    ),
    # Kołek ustalający złącza (drewniany trzpień). Dobiera go złączka przez
    # `dowel_sku` — połowa długości wchodzi w czoło jednej płyty, połowa
    # w płaszczyznę drugiej. Średnicę otworu bierze złączka
    # (`edge_hole_diameter_mm`), ale kołek jest osobną pozycją katalogową.
    "dowel": (
        "diameter_mm", "length_mm", "unit",
    ),
    # Kratka wentylacyjna wpuszczana w formatke (cokol, wieniec, plecy).
    # Kluczowe sa DWA wymiary, nie jeden: obrys widoczny i wyciecie w plycie.
    # Wyciecie na obrys to kratka wpadajaca do srodka, obrys na wyciecie to
    # szczelina po obwodzie - roznica u W80800 to 25 mm na dlugosci.
    "vent_grille": (
        "overall_length_mm", "overall_width_mm",
        "cutout_length_mm", "cutout_width_mm",
        "recess_depth_mm", "frame_thickness_mm",
        "free_area_cm2", "mounting_type", "unit",
    ),
    "furniture_accessory": ("accessory_type",),
}

# Pola systemu, których wprost potrzebują wiercenia i rozkrój w kalkulatorze
# (backend/hardware.py `_DRAWER_FIELDS` + okucia/compute.py).
DRAWER_SYSTEM_REQUIRED = (
    "name", "offset_prowadnica", "front_fix_offset_internal", "base_front_y",
    "fix_x_internal", "cut_bottom_width_reduction", "cut_bottom_depth_reduction",
    "cut_back_width_reduction", "available_nl_mm", "pricing_sku_prefix",
    "slide_screw_x_front_mm", "slide_screw_spacing_mm", "shelf_pin_x_offset_mm",
    "front_fix_second_hole_dy_mm", "front_fix_second_hole_min_h_mm",
    "carcass_dowel_x_offset_mm",
)

HINGE_SYSTEM_REQUIRED = (
    "name", "puszka_offset", "hinge_y_inset_mm", "cup_diameter_mm",
    "hinge_count_thresholds",
)

# Pola opcjonalne dla systemu, ale gdy ich brak — część funkcji się nie policzy.
DRAWER_SYSTEM_OPTIONAL_WITH_IMPACT = {
    "h_classes": "bez klas wysokości szuflady liczą się wzorem zachowawczym "
                 "(drawer_dims._without_h_classes) — wysokość ścianki jest szacowana",
    "side_thickness_mm": "brak grubości płaszcza systemowego",
    # Brak pola = 16 mm, czyli stan sprzed wariantów na płytę 18 (GTV AXIS PRO 18,
    # ATM Futura Evo). To nie jest kosmetyka: grubość decyduje o formatce dna
    # i tyłu, o wierceniach w nich i o tym, z którego arkusza schodzą.
    "box_board_thickness_mm": "brak grubości płyty szuflady — liczy się 16 mm",
    "rail_required_above_front_mm": "nie da się stwierdzić, czy front wymaga relingu",
}


def _is_empty(value) -> bool:
    """Puste = brak danej. `False` i `0` są poprawnymi wartościami."""
    if value is None:
        return True
    if isinstance(value, (str, list, tuple, dict)) and len(value) == 0:
        return True
    return False


def validate_item(item: dict) -> list:
    """Lista problemów jednej pozycji. Pusta = pozycja kompletna."""
    problems = []
    sku = item.get("sku")
    if not sku:
        problems.append("brak `sku`")
    category = item.get("category")
    if not category:
        problems.append("brak `category`")
        return problems
    if category not in REQUIRED_FIELDS:
        problems.append(f"kategoria {category!r} spoza słownika")
        return problems

    specs = item.get("specs") or {}
    na = set(specs.get("not_applicable") or ())
    for field in REQUIRED_FIELDS[category]:
        if field in na:
            continue
        if field not in specs:
            problems.append(f"brak wymaganego pola `{field}`")
        elif _is_empty(specs[field]):
            problems.append(f"pole `{field}` jest puste")
    return problems


def validate_system(system: dict) -> list:
    """Lista problemów jednego systemu (szuflad albo zawiasów)."""
    required = (HINGE_SYSTEM_REQUIRED if system.get("type") == "hinge"
                else DRAWER_SYSTEM_REQUIRED)
    problems = []
    for field in required:
        if field not in system:
            problems.append(f"brak wymaganego pola `{field}`")
        elif _is_empty(system[field]):
            problems.append(f"pole `{field}` jest puste")
    return problems


def validate_catalog(items=None, systems=None, hinge_systems=None) -> dict:
    """Pełny raport. Domyślnie sprawdza katalog wczytany przez loader.

    Zwraca:
      items_with_problems   {sku: [problemy]}
      systems_with_problems {id: [problemy]}
      unverified            SKU z `verified: false` — dane przeniesione z kodu,
                            niepotwierdzone kartą producenta
      degraded              systemy bez pól opcjonalnych, które coś psują
      ok                    czy nie ma twardych braków
    """
    from . import loader
    if items is None:
        items = loader.load_items()
    if systems is None:
        systems = loader.load_systems()
    if hinge_systems is None:
        hinge_systems = loader.load_hinge_systems()

    item_problems = {}
    for it in items:
        found = validate_item(it)
        if found:
            item_problems[it.get("sku") or "<bez sku>"] = found

    system_problems = {}
    degraded = {}
    for sid, s in {**systems, **hinge_systems}.items():
        found = validate_system(s)
        if found:
            system_problems[sid] = found
        if s.get("type") != "hinge":
            missing = {f: why for f, why in DRAWER_SYSTEM_OPTIONAL_WITH_IMPACT.items()
                       if _is_empty(s.get(f))}
            if missing:
                degraded[sid] = missing

    unverified = [it["sku"] for it in items
                  if (it.get("specs") or {}).get("verified") is False]

    return {
        "items_total": len(items),
        "items_with_problems": item_problems,
        "systems_with_problems": system_problems,
        "degraded_systems": degraded,
        "unverified": unverified,
        "ok": not item_problems and not system_problems,
    }
