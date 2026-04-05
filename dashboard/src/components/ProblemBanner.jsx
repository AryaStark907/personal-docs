import React from 'react'
export default function ProblemBanner({ problem }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-2xl p-5 flex items-start gap-4">
      <div className="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center flex-shrink-0 text-lg">🚨</div>
      <div className="flex-1">
        <div className="flex items-center gap-3 flex-wrap">
          <h2 className="text-sm font-semibold text-red-900">Primary Problem Detected</h2>
          <span className="text-xs bg-red-100 text-red-700 font-semibold px-2.5 py-1 rounded-full">{problem.metric} · {problem.change} WoW</span>
          <span className="text-xs bg-white text-red-600 border border-red-200 font-medium px-2.5 py-1 rounded-full">Stage: {problem.stage}</span>
        </div>
        <p className="text-sm text-red-700 mt-1.5">{problem.description}</p>
      </div>
    </div>
  )
}
