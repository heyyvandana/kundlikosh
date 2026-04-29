"""KundliKosh HTTP API — thin FastAPI wrapper around the engine.

Designed to be deployed free-tier on Render / Fly.io / Railway / HuggingFace Space.
Zero monthly cost while traffic stays small (engine is fast — ~50ms per chart).

Endpoints:
    POST /chart         — natal chart
    POST /dasha         — vimshottari mahadashas
    POST /yogas         — detected yogas
    POST /varga         — divisional charts (D9, D10, ...)
    POST /compatibility — ashtakoot guna milan
    POST /panchang      — 5-limb Vedic calendar for any date+location
    GET  /health
"""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from datetime import date as date_cls

from kundlikosh_engine import (
    chart_to_dict,
    compute_chart,
    compute_mahadashas,
    compute_panchang,
    compute_varga,
    current_dasha,
    dasha_timeline,
    detect_yogas,
    guna_milan,
)

app = FastAPI(
    title="KundliKosh API",
    version="0.1.0",
    description="Authentic Vedic astrology engine — sidereal Lahiri, free & open-source.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in prod once mobile app domain is known
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# --- Request models --------------------------------------------------------
class BirthInput(BaseModel):
    name: str = Field(default="Anonymous", max_length=80)
    date: str = Field(..., description="YYYY-MM-DD")
    time: str = Field(..., description="HH:MM (24h)")
    timezone: str = Field(default="Asia/Kolkata")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    use_lmt: bool = Field(default=False, description="Use Local Mean Time (pre-1906 historical births)")


class VargaInput(BirthInput):
    varga: str = Field(default="D9", description="One of D9, D10, D7, D3, D12")


class GunaMilanInput(BaseModel):
    bride: BirthInput
    groom: BirthInput


# --- Helpers ---------------------------------------------------------------
def _chart_from(payload: BirthInput):
    try:
        return compute_chart(
            name=payload.name,
            date=payload.date,
            time=payload.time,
            timezone_name=payload.timezone,
            latitude=payload.latitude,
            longitude=payload.longitude,
            use_lmt=payload.use_lmt,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"chart computation failed: {e}")


# --- Routes ----------------------------------------------------------------
@app.get("/health")
def health():
    return {"ok": True, "service": "kundlikosh-api", "version": app.version}


@app.post("/chart")
def chart(payload: BirthInput):
    return chart_to_dict(_chart_from(payload))


@app.post("/dasha")
def dasha(payload: BirthInput, num_mahadashas: int = 5):
    chart = _chart_from(payload)
    return {
        "current": current_dasha(chart),
        "timeline": dasha_timeline(chart, num_mahadashas=num_mahadashas),
    }


@app.post("/yogas")
def yogas(payload: BirthInput):
    chart = _chart_from(payload)
    return {"yogas": detect_yogas(chart)}


@app.post("/varga")
def varga(payload: VargaInput):
    chart = _chart_from(payload)
    try:
        v = compute_varga(chart, payload.varga.upper())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "name": v.name,
        "lagna_sign": v.lagna_sign,
        "lagna_sign_index": v.lagna_sign_index,
        "placements": v.placements,
    }


class PanchangInput(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD; the local-civil date you want panchang for")
    timezone: str = Field(default="Asia/Kolkata")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


@app.post("/panchang")
def panchang(payload: PanchangInput):
    try:
        on = date_cls.fromisoformat(payload.date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"invalid date: {e}")
    p = compute_panchang(
        on_date=on,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone_str=payload.timezone,
    )
    return p.to_dict()


@app.post("/compatibility")
def compatibility(payload: GunaMilanInput):
    bride = _chart_from(payload.bride)
    groom = _chart_from(payload.groom)
    result = guna_milan(bride, groom)
    return {
        "bride": result.bride,
        "groom": result.groom,
        "kootas": [
            {"name": k.name, "score": k.score, "max_score": k.max_score, "note": k.note}
            for k in result.kootas
        ],
        "total_score": result.total_score,
        "max_total": result.max_total,
        "bride_manglik": result.bride_manglik,
        "groom_manglik": result.groom_manglik,
        "manglik_balanced": result.manglik_balanced,
    }
