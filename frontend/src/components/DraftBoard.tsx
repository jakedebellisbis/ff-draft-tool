import React, { useMemo } from 'react'
import { League } from '../types'
import { snakePicks } from '../utils/snake'

type Props = {
  league: League
  keeperOverallPicks: number[]
  currentOverallPick: number
  onCurrentPickChange: (n: number) => void
}

export default function DraftBoard({ league, keeperOverallPicks, currentOverallPick, onCurrentPickChange }: Props) {
  const picks = useMemo(() => snakePicks(league.teams, league.draft_slot, Math.min(league.rounds, 20)), [league])

  return (
    <div style={{marginTop: 16}}>
      <div style={{display: 'flex', gap: 8, alignItems: 'center'}}>
        <label>Current Overall Pick:</label>
        <input type="number" min={1} value={currentOverallPick} onChange={e => onCurrentPickChange(Number(e.target.value))} />
      </div>
      <table style={{marginTop: 8, width: '100%', borderCollapse: 'collapse'}}>
        <thead>
          <tr>
            <th style={{textAlign:'left'}}>Round</th>
            <th style={{textAlign:'left'}}>My Overall</th>
            <th style={{textAlign:'left'}}>Note</th>
          </tr>
        </thead>
        <tbody>
          {picks.map((p, idx) => {
            const isKeeper = keeperOverallPicks.includes(p)
            return (
              <tr key={p} style={{background: isKeeper ? '#eee' : 'transparent'}}>
                <td>R{idx+1}</td>
                <td>{p}</td>
                <td>{isKeeper ? '(keeper)' : ''}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
