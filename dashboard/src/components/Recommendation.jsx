import React from 'react'
export default function Recommendation({ rec }) {
  return (
    <div className="bg-gradient-to-br from-indigo-600 to-violet-600 rounded-2xl p-6 text-white shadow-lg">
      <div className="flex items-center gap-2 mb-4"><span className="text-lg">🏆</span><h2 className="text-sm font-semibold opacity-90">Final Recommendation</h2></div>
      <h3 className="text-xl font-bold mb-2">{rec.experiment}</h3>
      <p className="text-sm opacity-80 mb-6">{rec.why}</p>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {[['Retention Lift',rec.retention_lift],['Engagement Lift',rec.engagement_lift],['Timeline',rec.timeline],['Secondary Exp.',rec.secondary]].map(([label,value]) => (
          <div key={label} className="bg-white/10 rounded-xl p-3"><p className="text-xs opacity-70 mb-1">{label}</p><p className="text-xs font-semibold">{value}</p></div>
        ))}
      </div>
      <div className="bg-white/10 rounded-xl p-4 flex items-start gap-3">
        <span className="flex-shrink-0">⚠️</span>
        <div><p className="text-xs font-semibold mb-0.5">Key Risk</p><p className="text-xs opacity-80">{rec.risk}</p></div>
      </div>
    </div>
  )
}
