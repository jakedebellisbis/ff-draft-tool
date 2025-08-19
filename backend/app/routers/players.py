from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from sqlalchemy import select, and_
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=List[schemas.PlayerWithADP])
def list_players(league_id: int = Query(...), adp_source: Optional[str] = Query(None), db: Session = Depends(get_db)):
    # If adp_source provided (e.g., Sleeper/ESPN/Yahoo), filter ADP by source
    # Otherwise, take the first ADP row if present (unspecified source)
    keepers = {k.player_id for k in db.query(models.Keeper).filter(models.Keeper.league_id==league_id).all()}

    if adp_source:
        # Join with ADP filtered by source
        stmt = (
            select(models.Player, models.ADP.adp)
            .join(models.ADP, and_(models.Player.id == models.ADP.player_id, models.ADP.league_id==league_id, models.ADP.source==adp_source), isouter=True)
        )
        rows = db.execute(stmt).all()
        out: List[schemas.PlayerWithADP] = []
        seen = set()
        for (player, adp) in rows:
            if player.id in seen: continue
            seen.add(player.id)
            out.append(schemas.PlayerWithADP(
                id=player.id, name=player.name, team=player.team, pos=player.pos,
                adp=adp, proj_points=player.proj_points, boom_pct=player.boom_pct,
                bust_pct=player.bust_pct, depth_chart=player.depth_chart,
                keeper=(player.id in keepers)
            ))
        return out
    else:
        # No source: left join without source filter
        stmt = (
            select(models.Player, models.ADP.adp)
            .join(models.ADP, and_(models.Player.id == models.ADP.player_id, models.ADP.league_id==league_id), isouter=True)
        )
        rows = db.execute(stmt).all()
        out: List[schemas.PlayerWithADP] = []
        seen = set()
        for (player, adp) in rows:
            if player.id in seen: continue
            seen.add(player.id)
            out.append(schemas.PlayerWithADP(
                id=player.id, name=player.name, team=player.team, pos=player.pos,
                adp=adp, proj_points=player.proj_points, boom_pct=player.boom_pct,
                bust_pct=player.bust_pct, depth_chart=player.depth_chart,
                keeper=(player.id in keepers)
            ))
        return out
