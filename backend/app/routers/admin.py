from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db, Base, engine
from .. import models

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/initdb")
def init_db(db: Session = Depends(get_db)):
    Base.metadata.create_all(bind=engine)
    return {"ok": True}
