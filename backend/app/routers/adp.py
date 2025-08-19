from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, List, Optional
from ..database import get_db
from .. import models

router = APIRouter(prefix="/adp", tags=["adp"])

@router.get("/consensus")
def consensus_adp(
    league_id: int,
    w_sleeper: float = 1.0,
    w_espn: float = 1.0,
    w_yahoo: float = 1.0,
    db: Session = Depends(get_db)
):
    """Return consensus ADP for each player in a league using weights for Sleeper/ESPN/Yahoo."""
    if not db.query(models.League).get(league_id):
        raise HTTPException(404, "League not found")
    rows = db.query(models.ADP).filter(models.ADP.league_id==league_id).all()
    # Aggregate by player_id
    res: Dict[int, Dict[str, float]] = {}
    for row in rows:
        pid = row.player_id
        if pid not in res:
            res[pid] = {"num": 0.0, "den": 0.0}
        if row.source.lower() == "sleeper":
            res[pid]["num"] += row.adp * w_sleeper
            res[pid]["den"] += w_sleeper
        elif row.source.lower() == "espn":
            res[pid]["num"] += row.adp * w_espn
            res[pid]["den"] += w_espn
        elif row.source.lower() == "yahoo":
            res[pid]["num"] += row.adp * w_yahoo
            res[pid]["den"] += w_yahoo
        else:
            # ignore unknown sources for now
            pass
    # Build list
    out = []
    for pid, agg in res.items():
        if agg["den"] > 0:
            out.append({"player_id": pid, "adp": agg["num"]/agg["den"]})
    return out
