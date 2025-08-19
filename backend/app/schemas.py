from pydantic import BaseModel
from typing import Optional, List

class PlayerBase(BaseModel):
    name: str
    team: Optional[str] = None
    pos: Optional[str] = None
    bye: Optional[int] = None
    age: Optional[int] = None
    proj_points: Optional[float] = None
    boom_pct: Optional[float] = None
    bust_pct: Optional[float] = None
    depth_chart: Optional[str] = None
    injury_status: Optional[str] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerOut(PlayerBase):
    id: int
    class Config:
        from_attributes = True

class LeagueBase(BaseModel):
    name: str
    teams: int = 10
    rounds: int = 16
    draft_slot: int = 1
    adp_sd: float = 12.0

class LeagueCreate(LeagueBase):
    pass

class LeagueOut(LeagueBase):
    id: int
    class Config:
        from_attributes = True

class ADPBase(BaseModel):
    league_id: int
    player_id: int
    adp: float
    source: str = "default"

class ADPCreate(ADPBase):
    pass

class ADPOut(ADPBase):
    id: int
    class Config:
        from_attributes = True

class KeeperBase(BaseModel):
    league_id: int
    player_id: int
    round: Optional[int] = None
    pick_in_round: Optional[int] = None
    overall_pick: Optional[int] = None

class KeeperCreate(KeeperBase):
    pass

class KeeperOut(KeeperBase):
    id: int
    class Config:
        from_attributes = True

class AvailabilityRequest(BaseModel):
    league_id: int
    current_overall_pick: int
    how_many: int = 200  # top N players to evaluate

class PlayerWithADP(BaseModel):
    id: int
    name: str
    team: Optional[str]
    pos: Optional[str]
    adp: Optional[float]
    proj_points: Optional[float] = None
    boom_pct: Optional[float] = None
    bust_pct: Optional[float] = None
    depth_chart: Optional[str] = None
    keeper: bool = False

class AvailabilityRow(BaseModel):
    player_id: int
    name: str
    adp: Optional[float]
    prob_next: Optional[float]
    prob_nextnext: Optional[float]
