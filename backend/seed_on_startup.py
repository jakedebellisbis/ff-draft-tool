from app.database import engine, SessionLocal
from app import models
from sqlalchemy.orm import Session

def seed():
    db: Session = SessionLocal()
    if db.query(models.League).count() == 0:  # only seed if empty
        league1 = models.League(
            name="League 1", teams=10, rounds=16, draft_slot=4, adp_sd=12.0
        )
        league2 = models.League(
            name="League 2", teams=10, rounds=16, draft_slot=9, adp_sd=12.0
        )
        db.add_all([league1, league2])
        db.commit()
        print("✅ Seeded initial leagues")
    else:
        print("ℹ️ Leagues already exist, skipping seed")

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    seed()
