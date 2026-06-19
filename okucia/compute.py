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
