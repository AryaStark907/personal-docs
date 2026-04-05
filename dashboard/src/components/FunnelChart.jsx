import React from 'react'
const COLORS = ['#6366f1','#818cf8','#a5b4fc','#c7d2fe']
export default function FunnelChart({ data }) {
  const max = data[0].users
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <div className="mb-6">
        <h2 className="text-sm font-semibold text-slate-900">Conversion Funnel</h2>
        <p className="text-xs text-slate-500 mt-0.5">Last 7 days</p>
      </div>
      <div className="space-y-3">
        {data.map((row,i) => {
          const pct = Math.round((row.users/max)*100)
          const convPct = i > 0 ? Math.round((row.users/data[i-1].users)*100) : null
          return (
            <div key={row.stage}>
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-xs font-medium text-slate-700">{row.stage}</span>
                <div className="flex items-center gap-2">
                  {convPct !== null && <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${convPct>=70?'bg-green-50 text-green-600':convPct>=50?'bg-amber-50 text-amber-600':'bg-red-50 text-red-600'}`}>{convPct}% conv.</span>}
                  <span className="text-xs text-slate-500">{row.users.toLocaleString()}</span>
                </div>
              </div>
              <div className="h-8 bg-slate-100 rounded-lg overflow-hidden">
                <div className="h-full rounded-lg flex items-center px-3" style={{ width:`${pct}%`, backgroundColor:COLORS[i] }}>
                  <span className="text-xs font-semibold text-white">{pct}%</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
