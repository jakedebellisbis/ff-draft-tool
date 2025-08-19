
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
import csv, io
from typing import Optional
from ..database import get_db
from .. import models

router = APIRouter(prefix="/import", tags=["import"])

def _player_by_name(db: Session, name: str):
    return db.query(models.Player).filter(models.Player.name==name).first()

@router.post("/players")
async def import_players_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    CSV columns (header required):
    name,team,pos,bye,age,proj_points,boom_pct,bust_pct,depth_chart,injury_status
    """
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    count = 0
    for row in reader:
        name = row.get("name")
        if not name:
            continue
        p = _player_by_name(db, name)
        if not p:
            p = models.Player(name=name)
        # Optional fields
        p.team = row.get("team") or p.team
        p.pos = row.get("pos") or p.pos
        p.bye = int(row["bye"]) if row.get("bye") else p.bye
        p.age = int(row["age"]) if row.get("age") else p.age
        p.proj_points = float(row["proj_points"]) if row.get("proj_points") else p.proj_points
        p.boom_pct = float(row["boom_pct"]) if row.get("boom_pct") else p.boom_pct
        p.bust_pct = float(row["bust_pct"]) if row.get("bust_pct") else p.bust_pct
        p.depth_chart = row.get("depth_chart") or p.depth_chart
        p.injury_status = row.get("injury_status") or p.injury_status
        db.add(p)
        count += 1
    db.commit()
    return {"ok": True, "imported": count}

@router.post("/adp")
async def import_adp_csv(
    league_id: int = Form(...),
    source: str = Form(...),  # "Sleeper" | "ESPN" | "Yahoo" (free text allowed)
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    CSV columns (header required):
    name,adp
    - 'name' must match Players.name exactly
    - 'adp' is numeric (overall pick)
    - 'source' form field tags the ADP provider (Sleeper/ESPN/Yahoo)
    """
    if not db.query(models.League).get(league_id):
        raise HTTPException(400, "League not found")
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    count = 0
    for row in reader:
        name = row.get("name")
        adp = row.get("adp")
        if not name or not adp:
            continue
        p = _player_by_name(db, name)
        if not p:
            # Optionally auto-create player stub
            p = models.Player(name=name)
            db.add(p); db.flush()
        # Upsert ADP
        existing = db.query(models.ADP).filter_by(league_id=league_id, player_id=p.id).first()
        if existing:
            existing.adp = float(adp)
            existing.source = source
        else:
            db.add(models.ADP(league_id=league_id, player_id=p.id, adp=float(adp), source=source))
        count += 1
    db.commit()
    return {"ok": True, "imported": count, "league_id": league_id, "source": source}

@router.post("/espn/analyst_ranks")
async def import_espn_analyst_ranks_csv(
    league_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    CSV columns (header required):
    name,analyst,overall_rank,pos_rank
    - 'name' maps to Players.name
    - 'analyst' is a string identifier (e.g., "Berry", "Karabell", "Yates")
    - overall_rank and pos_rank are numeric (pos_rank optional)
    """
    if not db.query(models.League).get(league_id):
        raise HTTPException(400, "League not found")
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    count = 0
    for row in reader:
        name = row.get("name")
        analyst = row.get("analyst")
        over = row.get("overall_rank")
        posr = row.get("pos_rank")
        if not name or not analyst:
            continue
        p = _player_by_name(db, name)
        if not p:
            p = models.Player(name=name)
            db.add(p); db.flush()
        ar = models.AnalystRank(
            league_id=league_id, player_id=p.id, source="ESPN", analyst=analyst,
            overall_rank=float(over) if over else None,
            pos_rank=float(posr) if posr else None
        )
        db.add(ar)
        count += 1
    db.commit()
    return {"ok": True, "imported": count, "league_id": league_id}
