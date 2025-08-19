import React from 'react'
import { League } from '../types'

type Props = {
  leagues: League[]
  selectedId?: number
  onChange: (id: number) => void
}

export default function LeagueSelector({ leagues, selectedId, onChange }: Props) {
  return (
    <div style={{display: 'flex', gap: 8, alignItems: 'center'}}>
      <label>League:</label>
      <select value={selectedId} onChange={e => onChange(Number(e.target.value))}>
        {leagues.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
      </select>
    </div>
  )
}
