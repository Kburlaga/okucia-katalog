"""
Logika liczona z systems.json — KANONICZNA (zastąpi rozjechane reguły
w cutting_list_v3.py / hardware.py kalkulatora w Fazie 3).

Konwencja:
  LW = światło korpusu (wewnętrzna szerokość sekcji), mm
  NL = długość nominalna prowadnicy, mm
  h_class = klasa wysokości szuflady: A / B / C / D
Płyta szuflady = 16 mm (standard GTV dla dna/tyłu).
"""
from . import loader

BOARD_MM = 16.0  # grubość płyty dna/tyłu


def pick_nl(depth_mm, system_id="gtv_axis_pro", clearance_mm=10.0):
    """Największe NL z katalogu, które zmieści się w korpusie o danej głębokości.
    Reguła GTV: szerokość/głębokość szuflady nie może przekraczać NL; zostawiamy
    margines `clearance_mm` na czoło/tylne mocowanie."""
    nls = sorted(loader.get_system(system_id).get("available_nl_mm", []))
    if not nls:
        raise ValueError(f"Brak available_nl_mm dla systemu {system_id!r}")
    fit = [n for n in nls if n <= depth_mm - clearance_mm]
    return fit[-1] if fit else nls[0]


def compute_drawer_parts(LW, NL, system_id="gtv_axis_pro", h_class="D",
                         front_height_mm=None):
    """Zwraca wymiary formatek + parametry montażowe pojedynczej szuflady.

    Wynik (mm):
      dno  = {width, depth, thickness}
      tyl  = {width, height, thickness}
      bok  = {thickness, height, length}   (metalowy płaszcz systemowy)
      offset_prowadnica, front_fix_offset_internal
      min_carcass_height, rail_required (bool|None)
    """
    sysd = loader.get_system(system_id)

    bottom_w = LW - sysd["cut_bottom_width_reduction"]
    bottom_d = NL - sysd["cut_bottom_depth_reduction"]
    back_w = LW - sysd["cut_back_width_reduction"]

    hc = (sysd.get("h_classes") or {}).get(h_class)
    if hc is None:
        raise KeyError(
            f"System {system_id!r} nie definiuje klasy {h_class!r}. "
            f"Dostępne: {sorted((sysd.get('h_classes') or {}).keys())}"
        )
    back_h = hc["real_mm"]
    side_h = hc["nominal_mm"]
    min_carcass_h = hc.get("min_carcass_height_mm")

    rail_threshold = sysd.get("rail_required_above_front_mm")
    rail_required = None
    if rail_threshold is not None and front_height_mm is not None:
        rail_required = front_height_mm > rail_threshold

    return {
        "system_id": system_id,
        "h_class": h_class,
        "LW": LW,
        "NL": NL,
        "dno": {"width": bottom_w, "depth": bottom_d, "thickness": BOARD_MM},
        "tyl": {"width": back_w, "height": back_h, "thickness": BOARD_MM},
        "bok": {
            "thickness": sysd.get("side_thickness_mm"),
            "height": side_h,
            "length": NL,
        },
        "offset_prowadnica": sysd["offset_prowadnica"],
        "front_fix_offset_internal": sysd["front_fix_offset_internal"],
        "min_carcass_height": min_carcass_h,
        "rail_required": rail_required,
    }


def pick_h_class(opening_mm, system_id="gtv_axis_pro"):
    """Dobiera klasę szuflady wg DOSTĘPNEJ wysokości w korpusie i minimalnej
    wysokości korpusu z danych technicznych (`min_carcass_height_mm`).

    Zwraca id najwyższej klasy, która się mieści (min_carcass_height ≤ opening),
    albo None gdy nawet najniższa się nie mieści / brak danych klas.
    """
    classes = (loader.get_system(system_id).get("h_classes") or {})
    fitting = [
        (cid, c["min_carcass_height_mm"])
        for cid, c in classes.items()
        if c.get("min_carcass_height_mm") is not None
        and c["min_carcass_height_mm"] <= opening_mm
    ]
    if not fitting:
        return None
    return max(fitting, key=lambda kv: kv[1])[0]


def compute_drawer_for_opening(LW, depth, opening_mm, system_id="gtv_axis_pro"):
    """Pełny dobór dla jednej szuflady w sekcji: NL z głębokości + klasa z miejsca
    w korpusie + wymiary formatek.

    Zwraca dict z wymiarami i `fits=True`, albo:
      - `fits=False` + `reason`/`min_required_mm` gdy szuflada się nie mieści,
      - `fits=None` + `reason` gdy system nie ma danych klas (do fallbacku).
    """
    sid = loader.resolve_system_id(system_id) or system_id
    sysd = loader.get_system(sid)
    nl = pick_nl(depth, sid)
    classes = sysd.get("h_classes") or {}
    if not classes:
        return {"fits": None, "system_id": sid, "NL": nl,
                "reason": f"System {sid} nie ma danych klas wysokości"}
    hc = pick_h_class(opening_mm, sid)
    if hc is None:
        min_needed = min(c["min_carcass_height_mm"] for c in classes.values()
                         if c.get("min_carcass_height_mm") is not None)
        return {"fits": False, "system_id": sid, "NL": nl,
                "min_required_mm": min_needed,
                "reason": (f"Na szufladę przypada {opening_mm:.0f} mm, a najniższa klasa "
                           f"wymaga min. {min_needed:.0f} mm wysokości korpusu")}
    parts = compute_drawer_parts(LW=LW, NL=nl, system_id=sid, h_class=hc,
                                 front_height_mm=opening_mm)
    parts["fits"] = True
    return parts
