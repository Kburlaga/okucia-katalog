"""
Auto-dobór towarzyszących okuć dla kompletu szuflady.

Port 1:1 logiki z Kalkulator_Stolarski_3/backend/hardware_matching.py,
zaadaptowany do formatu danych katalogu (item to dict z kluczem "specs"
będącym już dict-em, zamiast HardwareItem.specs_json jako string).

Dla danego SKU drawer_set zwraca SKU spójne technicznie i kolorystycznie:
- 2x connector (mount_position=inner_front) — złączki frontu wewnętrznego
- 2x connector (mount_position=back) — złączki ścianki tylnej
- 2x glass_panel (gdy drawer ma glass_sides=True)
Reling celowo NIE jest auto-dorzucany (świadoma opcja użytkownika).
"""
from typing import Any, Dict, List


def _specs(item) -> Dict[str, Any]:
    s = item.get("specs")
    return s if isinstance(s, dict) else {}


def match_drawer_accessories(drawer_sku: str, all_items: list) -> List[dict]:
    """Lista towarzyszących SKU dla danego kompletu szuflady (lub [] gdy brak)."""
    drawer = next((it for it in all_items if it.get("sku") == drawer_sku), None)
    if not drawer or drawer.get("category") != "drawer_set":
        return []

    d_specs = _specs(drawer)
    d_system = drawer.get("system_id")
    d_h_class = d_specs.get("h_drawer_class")
    d_color = d_specs.get("color_en")
    d_glass = bool(d_specs.get("glass_sides"))
    d_subsystem = d_specs.get("subsystem")

    results: List[dict] = []

    def _color_ok(s: Dict[str, Any]) -> bool:
        c = s.get("color_en")
        return c is None or d_color is None or c == d_color

    def _subsystem_ok(s: Dict[str, Any]) -> bool:
        # Tylko GLASS jest wykluczające (drawer glass <-> connector glass).
        c_is_glass = "glass" in (s.get("subsystem") or "")
        d_is_glass = "glass" in (d_subsystem or "")
        return c_is_glass == d_is_glass

    # --- Connectory: inner_front (2) i back (2) ---
    for it in all_items:
        if it.get("category") != "connector" or it.get("system_id") != d_system:
            continue
        s = _specs(it)
        if s.get("compatible_h_class") != d_h_class:
            continue
        if not _color_ok(s) or not _subsystem_ok(s):
            continue
        mp = s.get("mount_position")
        if mp == "inner_front":
            results.append({"sku": it["sku"], "name": it.get("name"),
                            "category": "connector", "qty": 2,
                            "reason": "Złączki frontu wewnętrznego (L+P)",
                            "color_pl": s.get("color_pl"), "h_value_mm": s.get("h_value_mm")})
        elif mp == "back":
            results.append({"sku": it["sku"], "name": it.get("name"),
                            "category": "connector", "qty": 2,
                            "reason": "Złączki ścianki tylnej (L+P)",
                            "color_pl": s.get("color_pl"), "h_value_mm": s.get("h_value_mm")})

    # --- Szklane boki (gdy drawer glass_sides) ---
    if d_glass:
        for it in all_items:
            if it.get("category") != "glass_panel" or it.get("system_id") != d_system:
                continue
            s = _specs(it)
            if s.get("compatible_h_class") != d_h_class or not _color_ok(s):
                continue
            results.append({"sku": it["sku"], "name": it.get("name"),
                            "category": "glass_panel", "qty": 2,
                            "reason": "Szklane boki szuflady (L+P)",
                            "color_pl": s.get("color_pl"),
                            "length_mm": s.get("length_mm"), "height_mm": s.get("height_mm")})

    return results
