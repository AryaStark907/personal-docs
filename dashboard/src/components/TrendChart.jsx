import React, { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
export default function TrendChart({ data }) {
  const [metric, setMetric] = useState('dau')
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-sm font-semibold text-slate-900">14-Day Trend</h2>
          <p className="text-xs text-slate-500 mt-0.5">Week-over-week comparison</p>
        </div>
        <div className="flex gap-1 bg-slate-100 rounded-lg p-1">
          {[['dau','DAU'],['session','Session Time']].map(([key,label]) => (
            <button key={key} onClick={() => setMetric(key)} className={`text-xs px-3 py-1.5 rounded-md font-medium transition-all ${metric===key ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}>{label}</button>
          ))}
        </div>
      </div>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data} margin={{ top:4, right:4, left:-20, bottom:0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey="day" tick={{ fontSize:11, fill:'#94a3b8' }} tickLine={false} axisLine={false} interval={1} />
          <YAxis tick={{ fontSize:11, fill:'#94a3b8' }} tickLine={false} axisLine={false} />
          <Tooltip contentStyle={{ border:'1px solid #e2e8f0', borderRadius:8, fontSize:12 }} labelStyle={{ fontWeight:600, color:'#1e293b' }} />
          <ReferenceLine x="D-7" stroke="#f59e0b" strokeDasharray="4 4" label={{ value:'This week', fontSize:10, fill:'#f59e0b', position:'top' }} />
          <Line type="monotone" dataKey={metric} stroke="#6366f1" strokeWidth={2.5} dot={false} activeDot={{ r:5, fill:'#6366f1', strokeWidth:0 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
