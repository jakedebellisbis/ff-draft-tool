from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..services import compute_overall

router = APIRouter(prefix="/keepers", tags=["keepers"])

@router.get("/", response_model=List[schemas.KeeperOut])
def list_keepers(league_id:int, db: Session = Depends(get_db)):
    return db.query(models.Keeper).filter(models.Keeper.league_id==league_id).all()

@router.post("/", response_model=schemas.KeeperOut)
def upsert_keeper(payload: schemas.KeeperCreate, db: Session = Depends(get_db)):
    # Ensure player & league exist
    league = db.query(models.League).get(payload.league_id)
    player = db.query(models.Player).get(payload.player_id)
    if not league or not player:
        raise HTTPException(400, "League or Player not found")
    # Compute overall if needed
    overall = payload.overall_pick
    if overall is None and payload.round and payload.pick_in_round:
        overall = compute_overall(league.teams, payload.round, payload.pick_in_round)
    # Upsert by (league_id, player_id)
    keeper = db.query(models.Keeper).filter_by(league_id=payload.league_id, player_id=payload.player_id).first()
    if keeper:
        keeper.round = payload.round
        keeper.pick_in_round = payload.pick_in_round
        keeper.overall_pick = overall
    else:
        keeper = models.Keeper(
            league_id=payload.league_id, player_id=payload.player_id,
            round=payload.round, pick_in_round=payload.pick_in_round, overall_pick=overall
        )
        db.add(keeper)
    db.commit()
    db.refresh(keeper)
    return keeper

@router.delete("/{keeper_id}")
def delete_keeper(keeper_id:int, db: Session = Depends(get_db)):
    k = db.query(models.Keeper).get(keeper_id)
    if not k: 
        raise HTTPException(404, "Not found")
    db.delete(k)
    db.commit()
    return {"ok": True}
