import math
from typing import List, Tuple

def snake_picks(num_teams:int, draft_slot:int, num_rounds:int) -> List[int]:
    picks = []
    for r in range(1, num_rounds+1):
        if r % 2 == 1:
            overall = (r-1)*num_teams + draft_slot
        else:
            overall = r*num_teams - (draft_slot-1)
        picks.append(overall)
    return picks

def compute_overall(num_teams:int, rnd:int, pick_in_round:int) -> int:
    if rnd % 2 == 0:
        return rnd*num_teams - (pick_in_round-1)
    return (rnd-1)*num_teams + pick_in_round

def next_two_picks(current_overall:int, my_picks:List[int]) -> Tuple[int, int]:
    nxt = min([p for p in my_picks if p > current_overall], default=None)
    nxt2 = min([p for p in my_picks if p > (nxt or 10**9)], default=None) if nxt else None
    return nxt, nxt2

def prob_available(adp:float, pick_overall:int, sd:float=12.0) -> float:
    if adp is None:
        return None
    z = ((pick_overall - 0.5) - adp) / sd
    # standard normal CDF
    return 1 - 0.5*(1 + math.erf(z / math.sqrt(2)))
