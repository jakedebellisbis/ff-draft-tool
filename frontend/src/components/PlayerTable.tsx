import React from 'react'
import { PlayerWithADP, AvailabilityRow } from '../types'

type Props = {
  players: PlayerWithADP[]
  availability: Record<number, AvailabilityRow | undefined>
}

function pct(n?: number | null) {
  if (n === null || n === undefined) return ''
  return (n*100).toFixed(0) + '%'
}

export default function PlayerTable({ players, availability }: Props) {
  return (
    <table style={{marginTop: 16, width: '100%', borderCollapse: 'collapse'}}>
      <thead>
        <tr>
          <th style={{textAlign:'left'}}>Player</th>
          <th>Pos</th>
          <th>Team</th>
          <th>ADP</th>
          <th>Depth</th>
          <th>Proj</th>
          <th>Boom</th>
          <th>Bust</th>
          <th>Next</th>
          <th>Next+1</th>
        </tr>
      </thead>
      <tbody>
        {players.map(p => {
          const av = availability[p.id]
          return (
            <tr key={p.id} style={{opacity: p.keeper ? 0.4 : 1}}>
              <td>{p.name}</td>
              <td style={{textAlign:'center'}}>{p.pos}</td>
              <td style={{textAlign:'center'}}>{p.team}</td>
              <td style={{textAlign:'center'}}>{p.adp ?? ''}</td>
              <td style={{textAlign:'center'}}>{p.depth_chart ?? ''}</td>
              <td style={{textAlign:'center'}}>{p.proj_points ?? ''}</td>
              <td style={{textAlign:'center'}}>{pct(p.boom_pct)}</td>
              <td style={{textAlign:'center'}}>{pct(p.bust_pct)}</td>
              <td style={{textAlign:'center'}} title="Probability player is still on board at your next pick">{pct(av?.prob_next)}</td>
              <td style={{textAlign:'center'}} title="Probability player is still on board at your next-next pick">{pct(av?.prob_nextnext)}</td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}
