import React from 'react'
const s = { High:'bg-red-50 text-red-600 border-red-200', Medium:'bg-amber-50 text-amber-600 border-amber-200', 'Low-Medium':'bg-slate-50 text-slate-600 border-slate-200' }
export default function RootCauses({ causes }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h2 className="text-sm font-semibold text-slate-900 mb-1">Root Cause Hypotheses</h2>
      <p className="text-xs text-slate-500 mb-5">Ranked by likelihood</p>
      <div className="space-y-3">
        {causes.map((c,i) => (
          <div key={c.id} className="flex items-start gap-4 p-4 bg-slate-50 rounded-xl">
            <div className="w-7 h-7 bg-white border border-slate-200 rounded-lg flex items-center justify-center text-xs font-bold text-slate-600 flex-shrink-0 shadow-sm">{i+1}</div>
            <p className="flex-1 text-sm text-slate-800">{c.text}</p>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border flex-shrink-0 ${s[c.likelihood]||s['Low-Medium']}`}>{c.likelihood}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
