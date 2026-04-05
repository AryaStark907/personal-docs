export const metrics = {
  prev_week: { avg_dau: 1821.4, avg_session_time: 416.9, avg_sessions: 3.13 },
  curr_week: { avg_dau: 1575.7, avg_session_time: 378.3, avg_sessions: 2.67 },
  wow_changes: { dau_pct: -13.49, session_time_pct: -9.25, sessions_pct: -14.61 },
}
export const retention = {
  d1: { prev: 42, curr: 36, wow_pct: -14.29 },
  d7: { prev: 18, curr: 14, wow_pct: -22.22 },
}
export const funnel = [
  { stage: 'Onboarding Start',    users: 5200 },
  { stage: 'Onboarding Complete', users: 3380 },
  { stage: 'Session 1',           users: 3200 },
  { stage: 'Session 2',           users: 1600 },
]
export const dailyTrend = [
  { day: 'D-14', dau: 1800, session: 420 },{ day: 'D-13', dau: 1850, session: 415 },
  { day: 'D-12', dau: 1820, session: 422 },{ day: 'D-11', dau: 1900, session: 418 },
  { day: 'D-10', dau: 1780, session: 410 },{ day: 'D-9',  dau: 1760, session: 408 },
  { day: 'D-8',  dau: 1840, session: 425 },{ day: 'D-7',  dau: 1650, session: 390 },
  { day: 'D-6',  dau: 1620, session: 385 },{ day: 'D-5',  dau: 1580, session: 378 },
  { day: 'D-4',  dau: 1600, session: 380 },{ day: 'D-3',  dau: 1540, session: 372 },
  { day: 'D-2',  dau: 1510, session: 368 },{ day: 'D-1',  dau: 1530, session: 375 },
]
export const problem = { metric: 'Day-7 Retention', change: '-22.2%', current: '14%', stage: 'Habit formation', description: 'Day-7 Retention dropped 22.2% WoW (now 14%), indicating weakening at the habit formation stage.' }
export const rootCauses = [
  { id: 'H1', likelihood: 'High',   text: 'No habit loop established — no streak, no social hook, no content cadence by day 7.' },
  { id: 'H2', likelihood: 'High',   text: 'Content / level progression runs dry for casual users within first week.' },
  { id: 'H3', likelihood: 'Medium', text: 'Email / push re-engagement missing or untargeted after day 2.' },
]
export const experiments = [
  { id:'EXP-01', rank:1, score:4.5, name:'Streak Shield — Daily Play Streak', inspired_by:'Duolingo', target:'Day-7 retention', retention_lift:'+3–5pp D7', engagement_lift:'+15% sessions/user', effort:'Medium', impact:'High', confidence:'High', description:'Visible daily streak counter + streak-at-risk push notification + one-time Streak Shield power-up.' },
  { id:'EXP-02', rank:2, score:4.5, name:'Lightning Onboarding — Win in 60s', inspired_by:'TikTok + Duolingo', target:'D1 retention & onboarding', retention_lift:'+2–4pp D1', engagement_lift:'+8% S1→S2', effort:'Medium', impact:'High', confidence:'High', description:'3-question quiz + guided mini-level under 60s. Delay sign-up until after first win.' },
  { id:'EXP-03', rank:3, score:2.0, name:'Dream Digest — Weekly Re-engagement', inspired_by:'Spotify + Roblox', target:'D7 & D14 retention', retention_lift:'+3–5pp D7', engagement_lift:'+20% at-risk WAU', effort:'Medium', impact:'Medium', confidence:'Medium', description:'Monday personalised push/email with Dream Stats + weekly content teaser + friends leaderboard.' },
  { id:'EXP-04', rank:4, score:1.33, name:'Smart Content Queue — Auto-next', inspired_by:'Netflix', target:'Session time', retention_lift:'+1–2pp D1 indirect', engagement_lift:'+10–15% session time', effort:'High', impact:'Medium', confidence:'Medium', description:'5-second countdown to next recommended item after content ends.' },
]
export const recommendation = { experiment:'EXP-01 — Streak Shield', why:'Highest priority score (4.5) — High impact on D7 retention, Medium effort, strong benchmark confidence from Duolingo.', retention_lift:'+3–5pp D7 retention', engagement_lift:'+15% sessions/user', timeline:'2-week build sprint + 2-week A/B measurement window', secondary:'EXP-02 — Lightning Onboarding', risk:'Push-notification dependency requires good opt-in rate. Pair with EXP-02 to request permission post first-win.' }
