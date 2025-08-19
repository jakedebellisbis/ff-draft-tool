from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    team = Column(String, index=True)
    pos = Column(String, index=True)
    bye = Column(Integer, nullable=True)
    age = Column(Integer, nullable=True)
    proj_points = Column(Float, nullable=True)
    boom_pct = Column(Float, nullable=True)
    bust_pct = Column(Float, nullable=True)
    depth_chart = Column(String, nullable=True)
    injury_status = Column(String, nullable=True)

    adps = relationship("ADP", back_populates="player")
    keepers = relationship("Keeper", back_populates="player")

class League(Base):
    __tablename__ = "leagues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    teams = Column(Integer, default=10)
    rounds = Column(Integer, default=16)
    draft_slot = Column(Integer, default=1)  # 1-indexed
    adp_sd = Column(Float, default=12.0)

    adps = relationship("ADP", back_populates="league")
    keepers = relationship("Keeper", back_populates="league")

class ADP(Base):
    __tablename__ = "adp"
    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    source = Column(String, default="default")
    adp = Column(Float)

    league = relationship("League", back_populates="adps")
    player = relationship("Player", back_populates="adps")
    __table_args__ = (UniqueConstraint("league_id", "player_id", "source", name="uq_league_player_source"),)

class Keeper(Base):
    __tablename__ = "keepers"
    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    round = Column(Integer, nullable=True)
    pick_in_round = Column(Integer, nullable=True)
    overall_pick = Column(Integer, nullable=True)  # computed or provided

    league = relationship("League", back_populates="keepers")
    player = relationship("Player", back_populates="keepers")
    __table_args__ = (UniqueConstraint("league_id", "player_id", name="uq_keeper_league_player"),)
