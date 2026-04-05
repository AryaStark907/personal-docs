import React from 'react'
const ec = { Low:'text-green-600 bg-green-50', Medium:'text-amber-600 bg-amber-50', High:'text-red-600 bg-red-50' }
const ic = { Low:'text-slate-600 bg-slate-50', Medium:'text-blue-600 bg-blue-50', High:'text-indigo-600 bg-indigo-50' }
const em = { Duolingo:'🦉', Netflix:'🎬', Spotify:'🎵', Roblox:'🎮', 'TikTok + Duolingo':'📱', 'Spotify + Roblox':'🎯' }
export default function Experiments({ experiments }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h2 className="text-sm font-semibold text-slate-900 mb-1">Experiments</h2>
      <p className="text-xs text-slate-500 mb-5">Ranked by Impact × Confidence ÷ Effort</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {experiments.map(exp => (
          <div key={exp.id} className={`rounded-xl border p-5 relative overflow-hidden ${exp.rank===1?'border-indigo-200 bg-indigo-50/40':'border-slate-200 bg-slate-50/40'}`}>
            {exp.rank===1 && <span className="absolute top-3 right-3 text-xs bg-indigo-600 text-white font-semibold px-2 py-0.5 rounded-full">Top Pick</span>}
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold text-slate-400">#{exp.rank}</span>
              <span className="text-xs text-slate-500 font-medium">{exp.id}</span>
              <span className="text-xs font-semibold text-slate-600 bg-white border border-slate-200 px-2 py-0.5 rounded-full">Score {exp.score}</span>
            </div>
            <h3 className="text-sm font-semibold text-slate-900 mb-1 pr-16">{exp.name}</h3>
            <p className="text-xs text-slate-500 mb-3">{exp.description}</p>
            <div className="flex flex-wrap gap-2 mb-3">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${ic[exp.impact]}`}>Impact: {exp.impact}</span>
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${ec[exp.effort]}`}>Effort: {exp.effort}</span>
            </div>
            <div className="border-t border-slate-200 pt-3 grid grid-cols-2 gap-2">
              <div><p className="text-xs text-slate-400 mb-0.5">Retention lift</p><p className="text-xs font-semibold text-slate-700">{exp.retention_lift}</p></div>
              <div><p className="text-xs text-slate-400 mb-0.5">Engagement lift</p><p className="text-xs font-semibold text-slate-700">{exp.engagement_lift}</p></div>
            </div>
            <div className="mt-3 flex items-center gap-1.5">
              <span>{em[exp.inspired_by]||'💡'}</span>
              <span className="text-xs text-slate-500">Inspired by <span className="font-medium text-slate-700">{exp.inspired_by}</span></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
