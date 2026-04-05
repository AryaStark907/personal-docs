import React from 'react'
function Badge({ value }) {
  const neg = value < 0
  return <span className={`inline-flex items-center text-xs font-semibold px-2 py-0.5 rounded-full ${neg ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>{neg ? '▼' : '▲'} {Math.abs(value).toFixed(1)}%</span>
}
function Card({ label, current, prev, wow, unit='', format }) {
  const display = format ? format(current) : `${current}${unit}`
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">{label}</p>
      <p className="text-3xl font-bold text-slate-900 mt-2">{display}</p>
      <div className="flex items-center gap-2 mt-3">
        <Badge value={wow} />
        <span className="text-xs text-slate-400">vs {format ? format(prev) : `${prev}${unit}`} prev week</span>
      </div>
    </div>
  )
}
export default function MetricCards({ metrics, retention }) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <Card label="Daily Active Users" current={Math.round(metrics.curr_week.avg_dau)} prev={Math.round(metrics.prev_week.avg_dau)} wow={metrics.wow_changes.dau_pct} format={v => v.toLocaleString()} />
      <Card label="Avg Session Time" current={Math.round(metrics.curr_week.avg_session_time)} prev={Math.round(metrics.prev_week.avg_session_time)} wow={metrics.wow_changes.session_time_pct} format={v => `${Math.floor(v/60)}m ${v%60}s`} />
      <Card label="Day-1 Retention" current={retention.d1.curr} prev={retention.d1.prev} wow={retention.d1.wow_pct} unit="%" />
      <Card label="Day-7 Retention" current={retention.d7.curr} prev={retention.d7.prev} wow={retention.d7.wow_pct} unit="%" />
    </div>
  )
}
