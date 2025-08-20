from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["leagues"])

@router.post("/", response_model=schemas.LeagueOut)
def create_league(payload: schemas.LeagueCreate, db: Session = Depends(get_db)):
    league = models.League(**payload.model_dump())
    db.add(league)
    db.commit()
    db.refresh(league)
    return league

@router.get("/", response_model=List[schemas.LeagueOut])
def list_leagues(db: Session = Depends(get_db)):
    return db.query(models.League).all()

@router.get("/{league_id}", response_model=schemas.LeagueOut)
def get_league(league_id: int, db: Session = Depends(get_db)):
    league = db.get(models.League, league_id)  # SQLAlchemy 2.x style
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league

