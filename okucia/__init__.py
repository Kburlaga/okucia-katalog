"""
okucia — wydzielony katalog okuć meblowych (dane + logika), współdzielony.

Krok 1: „bliźniak" dla Fusion (czysty Python, bez web/DB). Docelowo to samo
jądro owijamy w serwis HTTP i podpinamy pod kalkulator stolarski — jeden
katalog aktualizowany w jednym miejscu.

Użycie:
    from okucia import compute, matching, loader
    parts = compute.compute_drawer_parts(LW=573, NL=550,
                                         system_id='gtv_axis_pro', h_class='D')
"""
from . import loader, compute, matching  # noqa: F401

__all__ = ["loader", "compute", "matching"]
__version__ = "0.1.0"
