"""
okucia-service — cienka warstwa HTTP nad pakietem `okucia`.

Serwuje katalog + logikę przez REST, żeby korzystać mogły z niej programy
nie-Pythonowe i zdalne (Fusion z PC po LAN, kalkulator stolarski, inne).
Read-only — brak zapisu, brak logowania (zasób wewnętrzny w sieci lokalnej).

Uruchomienie lokalne:  uvicorn app:app --reload --port 8000
"""
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from okucia import compute, loader, matching, __version__

app = FastAPI(title="okucia-katalog", version=__version__,
              description="Wspólny katalog okuć meblowych (dane + logika).")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "version": __version__}


@app.get("/systems")
def systems():
    return loader.load_systems()


@app.get("/systems/{system_id}")
def system(system_id: str):
    try:
        return loader.get_system(system_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/items")
def items(category: Optional[str] = None, system_id: Optional[str] = None):
    return loader.load_items(category=category, system_id=system_id)


@app.get("/items/{sku}")
def item(sku: str):
    it = loader.get_item(sku)
    if it is None:
        raise HTTPException(status_code=404, detail=f"Nieznane SKU: {sku}")
    return it


@app.get("/items/{sku}/related")
def related(sku: str):
    """Auto-dobrane akcesoria (złączki/szkło) dla kompletu szuflady."""
    return matching.match_drawer_accessories(sku, loader.load_items())


@app.get("/compute/drawer")
def compute_drawer(
    lw: float = Query(..., description="światło korpusu (wewn. szerokość), mm"),
    system_id: str = "gtv_axis_pro",
    h_class: str = "D",
    nl: Optional[float] = Query(None, description="długość prowadnicy; gdy brak — z depth"),
    depth: Optional[float] = Query(None, description="głębokość korpusu (do auto-doboru NL)"),
    front_h: Optional[float] = Query(None, description="wysokość frontu (do oceny relingu)"),
):
    """Wymiary formatek szuflady wg wzorów systemu."""
    try:
        if nl is None:
            if depth is None:
                raise HTTPException(status_code=400, detail="Podaj `nl` albo `depth`.")
            nl = compute.pick_nl(depth, system_id)
        return compute.compute_drawer_parts(LW=lw, NL=nl, system_id=system_id,
                                            h_class=h_class, front_height_mm=front_h)
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
