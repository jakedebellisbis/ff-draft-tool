import React, { useMemo, useState } from 'react'
import { api } from '../api/client'
import { League } from '../types'

type Props = { leagues: League[] }

export default function ImportPage({ leagues }: Props) {
  const [leagueId, setLeagueId] = useState<number | undefined>(leagues[0]?.id)
  const [playersFile, setPlayersFile] = useState<File | null>(null)
  const [adpFile, setAdpFile] = useState<File | null>(null)
  const [adpSource, setAdpSource] = useState<'Sleeper' | 'ESPN' | 'Yahoo'>('Sleeper')
  const [espnFile, setEspnFile] = useState<File | null>(null)
  const [message, setMessage] = useState<string>('')

  const ready = useMemo(() => !!leagueId, [leagueId])

  async function uploadPlayers() {
    if (!playersFile) return setMessage('Select a players CSV first.')
    const form = new FormData()
    form.append('file', playersFile)
    const res = await api.post('/import/players', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    setMessage(JSON.stringify(res.data))
  }

  async function uploadADP() {
    if (!adpFile || !leagueId) return setMessage('Pick a league and ADP CSV first.')
    const form = new FormData()
    form.append('league_id', String(leagueId))
    form.append('source', adpSource)
    form.append('file', adpFile)
    const res = await api.post('/import/adp', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    setMessage(JSON.stringify(res.data))
  }

  async function uploadEspnRanks() {
    if (!espnFile || !leagueId) return setMessage('Pick a league and ESPN ranks CSV first.')
    const form = new FormData()
    form.append('league_id', String(leagueId))
    form.append('file', espnFile)
    const res = await api.post('/import/espn/analyst_ranks', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    setMessage(JSON.stringify(res.data))
  }

  return (
    <div style={{display:'grid', gap: 24}}>
      <div style={{display:'flex', gap: 8, alignItems:'center'}}>
        <label>League:</label>
        <select value={leagueId} onChange={e => setLeagueId(Number(e.target.value))}>
          {leagues.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
        </select>
      </div>

      <section style={{border:'1px solid #ccc', padding: 12, borderRadius: 8}}>
        <h3>Upload Players</h3>
        <p>CSV header: <code>name,team,pos,bye,age,proj_points,boom_pct,bust_pct,depth_chart,injury_status</code></p>
        <input type="file" accept=".csv" onChange={e => setPlayersFile(e.target.files?.[0] || null)} />
        <button onClick={uploadPlayers} disabled={!ready}>Upload</button>
      </section>

      <section style={{border:'1px solid #ccc', padding: 12, borderRadius: 8}}>
        <h3>Upload ADP (Sleeper/ESPN/Yahoo)</h3>
        <p>CSV header: <code>name,adp</code></p>
        <div style={{display:'flex', gap: 8, alignItems:'center'}}>
          <label>Source:</label>
          <select value={adpSource} onChange={e => setAdpSource(e.target.value as any)}>
            <option value="Sleeper">Sleeper</option>
            <option value="ESPN">ESPN</option>
            <option value="Yahoo">Yahoo</option>
          </select>
        </div>
        <input type="file" accept=".csv" onChange={e => setAdpFile(e.target.files?.[0] || null)} />
        <button onClick={uploadADP} disabled={!ready}>Upload</button>
      </section>

      <section style={{border:'1px solid #ccc', padding: 12, borderRadius: 8}}>
        <h3>Upload ESPN Host Ranks</h3>
        <p>CSV header: <code>name,analyst,overall_rank,pos_rank</code></p>
        <input type="file" accept=".csv" onChange={e => setEspnFile(e.target.files?.[0] || null)} />
        <button onClick={uploadEspnRanks} disabled={!ready}>Upload</button>
      </section>

      {message && <pre style={{whiteSpace:'pre-wrap', background:'#f7f7f7', padding:8, borderRadius:6}}>{message}</pre>}
    </div>
  )
}
