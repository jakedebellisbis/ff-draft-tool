from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select
from .. import models, schemas
from ..database import get_db
from ..services import snake_picks, next_two_picks, prob_available

router = APIRouter(prefix="/availability", tags=["availability"])

@router.post("/", response_model=List[schemas.AvailabilityRow])
def compute_availability(payload: schemas.AvailabilityRequest, db: Session = Depends(get_db)):
    league = db.query(models.League).get(payload.league_id)
    if not league:
        raise HTTPException(404, "League not found")

    # Build my pick list and get next two
    my_picks = snake_picks(league.teams, league.draft_slot, league.rounds)
    nxt, nxt2 = next_two_picks(payload.current_overall_pick, my_picks)
    if not nxt:
        return []

    # Pull top N players with ADP for this league, excluding keepers
    keepers = {k.player_id for k in db.query(models.Keeper).filter_by(league_id=league.id).all()}
    stmt = (
        select(models.Player, models.ADP.adp)
        .join(models.ADP, models.Player.id == models.ADP.player_id, isouter=True)
        .where((models.ADP.league_id == league.id) | (models.ADP.league_id.is_(None)))
        .limit(payload.how_many)
    )
    rows = db.execute(stmt).all()

    out = []
    for player, adp in rows:
        if player.id in keepers:
            continue
        prob1 = prob_available(adp, nxt, sd=league.adp_sd) if adp is not None else None
        prob2 = prob_available(adp, nxt2, sd=league.adp_sd) if (adp is not None and nxt2) else None
        out.append(schemas.AvailabilityRow(
            player_id = player.id, name = player.name, adp = adp,
            prob_next = prob1, prob_nextnext = prob2
        ))
    # Sort by prob_next desc, then proj_points if available
    out.sort(key=lambda r: (r.prob_next or -1, ), reverse=True)
    return out
