export type League = {
  id: number
  name: string
  teams: number
  rounds: number
  draft_slot: number
  adp_sd: number
}

export type PlayerWithADP = {
  id: number
  name: string
  team?: string
  pos?: string
  adp?: number | null
  proj_points?: number | null
  boom_pct?: number | null
  bust_pct?: number | null
  depth_chart?: string | null
  keeper: boolean
}

export type AvailabilityRow = {
  player_id: number
  name: string
  adp?: number | null
  prob_next?: number | null
  prob_nextnext?: number | null
}
