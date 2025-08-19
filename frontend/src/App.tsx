import React, { useEffect, useMemo, useState } from 'react'
import { api } from './api/client'
import LeagueSelector from './components/LeagueSelector'
import DraftBoard from './components/DraftBoard'
import PlayerTable from './components/PlayerTable'
import ImportPage from './components/ImportPage'
import { League, PlayerWithADP, AvailabilityRow } from './types'

type ADPSource = 'Sleeper' | 'ESPN' | 'Yahoo' | 'Consensus'

export default function App() {
  const [tab, setTab] = useState<'Draft'|'Imports'>('Draft')
  const [leagues, setLeagues] = useState<League[]>([])
  const [leagueId, setLeagueId] = useState<number | undefined>(undefined)
  const [league, setLeague] = useState<League | undefined>(undefined)
  const [players, setPlayers] = useState<PlayerWithADP[]>([])
  const [keepers, setKeepers] = useState<number[]>([])
  const [currentPick, setCurrentPick] = useState(1)
  const [availability, setAvailability] = useState<Record<number, AvailabilityRow>>({})
  const [adpSource, setAdpSource] = useState<ADPSource>('Sleeper')
  const [consensus, setConsensus] = useState<Record<number, number>>({})

  // Load leagues on mount
  useEffect(() => {
    api.get('/leagues').then(res => {
      setLeagues(res.data)
      if (res.data.length) {
        setLeagueId(res.data[0].id)
      }
    })
  }, [])

  // Load league details and base data when leagueId or adpSource changes
  useEffect(() => {
    if (!leagueId) return
    api.get(`/leagues/${leagueId}`).then(res => setLeague(res.data))
    // Fetch players with selected adpSource (unless Consensus; we overlay separately)
    const params: any = { league_id: leagueId }
    if (adpSource !== 'Consensus') params.adp_source = adpSource
    api.get('/players', { params }).then(res => setPlayers(res.data))
    // Keepers
    api.get('/keepers', { params: { league_id: leagueId }}).then(res => {
      const picks = (res.data as any[]).map(k => k.overall_pick).filter((n: number | null) => !!n)
      setKeepers(picks)
    })
    // Consensus overlay if needed
    if (adpSource === 'Consensus') {
      api.get('/adp/consensus', { params: { league_id: leagueId }}).then(res => {
        const map: Record<number, number> = {}
        for (const r of res.data as any[]) map[r.player_id] = r.adp
        setConsensus(map)
      })
    } else {
      setConsensus({})
    }
  }, [leagueId, adpSource])

  // Compute availability when inputs change
  useEffect(() => {
    if (!leagueId) return
    api.post('/availability', { league_id: leagueId, current_overall_pick: currentPick, how_many: 500 })
      .then(res => {
        const map: Record<number, AvailabilityRow> = {}
        for (const row of res.data as AvailabilityRow[]) map[row.player_id] = row
        setAvailability(map)
      })
  }, [leagueId, currentPick])

  const keeperPicks = useMemo(() => keepers.filter(Boolean) as number[], [keepers])

  // If consensus, overlay adp values
  const displayPlayers = useMemo(() => {
    if (adpSource !== 'Consensus') return players
    return players.map(p => ({ ...p, adp: consensus[p.id] ?? p.adp }))
  }, [players, consensus, adpSource])

  if (!league || !leagueId) return <div style={{padding: 24}}>Loading…</div>

  return (
    <div style={{padding: 24, display: 'grid', gap: 16, maxWidth: 1100, margin: '0 auto'}}>
      <h1>Fantasy Draft Tool</h1>

      <div style={{display: 'flex', gap: 16, flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between'}}>
        <LeagueSelector leagues={leagues} selectedId={leagueId} onChange={setLeagueId} />
        <div style={{display:'flex', gap: 8, alignItems:'center'}}>
          <label>ADP Source:</label>
          <select value={adpSource} onChange={e => setAdpSource(e.target.value as ADPSource)}>
            <option value="Sleeper">Sleeper</option>
            <option value="ESPN">ESPN</option>
            <option value="Yahoo">Yahoo</option>
            <option value="Consensus">Consensus</option>
          </select>
        </div>
        <div style={{display:'flex', gap:8}}>
          <button onClick={() => setTab('Draft')} disabled={tab==='Draft'}>Draft</button>
          <button onClick={() => setTab('Imports')} disabled={tab==='Imports'}>Imports</button>
        </div>
      </div>

      {tab === 'Draft' ? (
        <>
          <DraftBoard league={league} keeperOverallPicks={keeperPicks} currentOverallPick={currentPick} onCurrentPickChange={setCurrentPick} />
          <PlayerTable players={displayPlayers} availability={availability} />
        </>
      ) : (
        <ImportPage leagues={leagues} />
      )}
    </div>
  )
}
