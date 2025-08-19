# Seed a tiny dataset so the app boots with example data.
from .database import Base, engine, SessionLocal
from . import models

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Leagues
    l1 = models.League(name="League 1", teams=10, rounds=16, draft_slot=4, adp_sd=12.0)
    l2 = models.League(name="League 2", teams=10, rounds=16, draft_slot=9, adp_sd=12.0)
    db.add_all([l1, l2])
    db.commit(); db.refresh(l1); db.refresh(l2)

    # Players (subset)
    players = [
        models.Player(name="Christian McCaffrey", team="SF", pos="RB", proj_points=320, boom_pct=0.45, bust_pct=0.12, depth_chart="RB1"),
        models.Player(name="CeeDee Lamb", team="DAL", pos="WR", proj_points=300, boom_pct=0.40, bust_pct=0.15, depth_chart="WR1"),
        models.Player(name="Justin Jefferson", team="MIN", pos="WR", proj_points=305, boom_pct=0.42, bust_pct=0.14, depth_chart="WR1"),
        models.Player(name="Bijan Robinson", team="ATL", pos="RB", proj_points=280, boom_pct=0.38, bust_pct=0.18, depth_chart="RB1"),
        models.Player(name="Amon-Ra St. Brown", team="DET", pos="WR", proj_points=285, boom_pct=0.36, bust_pct=0.16, depth_chart="WR1"),
        models.Player(name="Breece Hall", team="NYJ", pos="RB", proj_points=275, boom_pct=0.37, bust_pct=0.19, depth_chart="RB1"),
        models.Player(name="Ja'Marr Chase", team="CIN", pos="WR", proj_points=295, boom_pct=0.39, bust_pct=0.17, depth_chart="WR1"),
        models.Player(name="A.J. Brown", team="PHI", pos="WR", proj_points=270, boom_pct=0.35, bust_pct=0.18, depth_chart="WR1"),
        models.Player(name="Jonathan Taylor", team="IND", pos="RB", proj_points=260, boom_pct=0.33, bust_pct=0.20, depth_chart="RB1"),
        models.Player(name="Garrett Wilson", team="NYJ", pos="WR", proj_points=255, boom_pct=0.34, bust_pct=0.21, depth_chart="WR1"),
    ]
    db.add_all(players); db.commit()
    # ADP by league
    adps_l1 = [1.8, 3.2, 2.5, 5.5, 6.0, 7.2, 4.8, 8.5, 14.0, 12.0]
    adps_l2 = [2.1, 3.8, 2.9, 6.1, 6.8, 7.6, 5.1, 9.1, 13.0, 12.5]

    # Fetch players with ids
    plist = db.query(models.Player).all()
    for p, a1, a2 in zip(plist, adps_l1, adps_l2):
        db.add(models.ADP(league_id=l1.id, player_id=p.id, adp=a1, source="ADP_L1"))
        db.add(models.ADP(league_id=l2.id, player_id=p.id, adp=a2, source="ADP_L2"))
    db.commit()

    # Example keeper (League 1 keeps Jonathan Taylor at overall 14)
    jt = db.query(models.Player).filter_by(name="Jonathan Taylor").first()
    db.add(models.Keeper(league_id=l1.id, player_id=jt.id, overall_pick=14))
    db.commit()
    db.close()

if __name__ == "__main__":
    run()
