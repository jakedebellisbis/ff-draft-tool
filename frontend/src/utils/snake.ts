export function snakePicks(teams: number, slot: number, rounds: number): number[] {
  const picks: number[] = []
  for (let r = 1; r <= rounds; r++) {
    if (r % 2 === 1) picks.push((r-1)*teams + slot)
    else picks.push(r*teams - (slot-1))
  }
  return picks
}
