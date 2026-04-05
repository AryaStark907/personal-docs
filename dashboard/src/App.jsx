import React from 'react'
import MetricCards from './components/MetricCards'
import TrendChart from './components/TrendChart'
import FunnelChart from './components/FunnelChart'
import ProblemBanner from './components/ProblemBanner'
import RootCauses from './components/RootCauses'
import Experiments from './components/Experiments'
import Recommendation from './components/Recommendation'
import { metrics, retention, funnel, dailyTrend, problem, rootCauses, experiments, recommendation } from './data'
export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 px-8 py-5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-slate-900">DreamPlay Analytics</h1>
            <p className="text-sm text-slate-500 mt-0.5">Product Growth Dashboard · Last 14 days</p>
          </div>
          <span className="text-xs bg-amber-50 text-amber-700 border border-amber-200 px-3 py-1.5 rounded-full font-medium">Mock data — connect BigQuery for live metrics</span>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-8 py-8 space-y-8">
        <ProblemBanner problem={problem} />
        <MetricCards metrics={metrics} retention={retention} />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <TrendChart data={dailyTrend} />
          <FunnelChart data={funnel} />
        </div>
        <RootCauses causes={rootCauses} />
        <Experiments experiments={experiments} />
        <Recommendation rec={recommendation} />
      </main>
      <footer className="text-center text-xs text-slate-400 py-6 border-t border-slate-200 mt-4">DreamPlay Autonomous Product Growth Agent · Powered by Claude</footer>
    </div>
  )
}
