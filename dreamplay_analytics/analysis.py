"""
STEP 3-7 — Hypotheses, benchmarks, experiments, impact, prioritisation.
"""

from __future__ import annotations
from typing import Any

HYPOTHESIS_BANK = {
    "Day-1 Retention": [
        {"id":"H1","hypothesis":"Onboarding flow is too long — users drop before experiencing core value.","likelihood":"High","signals":["Onboarding completion ~65%","D1 ret dropped 14% WoW"]},
        {"id":"H2","hypothesis":"First session ends without a win moment — users never feel accomplished.","likelihood":"High","signals":["Session-1→2 rate only 50%","avg session time falling"]},
        {"id":"H3","hypothesis":"Push-notification permission prompt shown too early, causing denial.","likelihood":"Medium","signals":["D1 drop correlates with notification opt-out patterns"]},
        {"id":"H4","hypothesis":"Recent update attracted less-engaged cohort (paid UA or seasonal shift).","likelihood":"Medium","signals":["DAU down 14% but could be mix shift"]},
        {"id":"H5","hypothesis":"Performance regression in last release degrading first impression.","likelihood":"Low-Medium","signals":["Need session_logs crash/latency data to confirm"]},
    ],
    "Day-7 Retention": [
        {"id":"H1","hypothesis":"No habit loop established — no streak, no social hook, no content cadence by day 7.","likelihood":"High","signals":["D7 ret at 14%, below 20% mobile gaming benchmark"]},
        {"id":"H2","hypothesis":"Content / level progression runs dry for casual users within first week.","likelihood":"High","signals":["session depth drop-off steep after session 3"]},
        {"id":"H3","hypothesis":"Email / push re-engagement missing or untargeted after day 2.","likelihood":"Medium","signals":["Common cause of D3-D7 churn in mobile apps"]},
    ],
}

_FALLBACK_HYPOTHESES = [
    {"id":"H1","hypothesis":"Onboarding friction preventing users from reaching core value proposition.","likelihood":"High","signals":["Onboarding completion 65%","D1 retention dropped"]},
    {"id":"H2","hypothesis":"Missing habit-forming mechanic (streak/social) causes day 3-7 churn.","likelihood":"High","signals":["D7 retention 14% vs 20% benchmark"]},
    {"id":"H3","hypothesis":"Session 1→2 conversion (50%) indicates weak aha moment delivery.","likelihood":"Medium","signals":["50% S1→S2 rate, below 65% target"]},
    {"id":"H4","hypothesis":"Push notification permission requested at wrong moment.","likelihood":"Medium","signals":["Industry data: timing matters ±20% opt-in rate"]},
    {"id":"H5","hypothesis":"Recent release introduced latency / stability regression.","likelihood":"Low-Medium","signals":["Needs crash + latency log review"]},
]

BENCHMARKS = [
    {"company":"Duolingo","problem_solved":"Low D1/D7 retention","what_they_changed":"Daily streak counter, streak-at-risk push notifications, win within 90s onboarding.","why_it_worked":"Streaks create loss aversion. Quick win lowers perceived cost of return.","applicability_to_dreamplay":"Adopt daily play streak + dream streak at risk notification.","reported_impact":"+20% D7 retention after streak introduction"},
    {"company":"Netflix","problem_solved":"First-session drop-off / content paralysis","what_they_changed":"Auto-plays next episode within 5s, personalises home row from session 1.","why_it_worked":"Reduces decision fatigue. Personalisation signals product knows the user.","applicability_to_dreamplay":"Surface personalised For You row after onboarding; auto-queue next content.","reported_impact":"Reduced subscriber churn ~8% via continue-watching prompts"},
    {"company":"Spotify","problem_solved":"Session depth and habit formation","what_they_changed":"Wrapped recap, Daily Mix, Discover Weekly — all automated and personalised.","why_it_worked":"Gives users a reason to return every week and creates shareable identity.","applicability_to_dreamplay":"Weekly Dream Digest — personalised recap delivered Monday morning.","reported_impact":"Discover Weekly drove 40M+ monthly listeners within 2 months"},
    {"company":"TikTok","problem_solved":"Cold-start onboarding and session time","what_they_changed":"Skip sign-up for first session; prompt only after 3 videos watched.","why_it_worked":"Removes all friction before value delivery. User is hooked before sign-up.","applicability_to_dreamplay":"Allow guest play for first session; prompt account creation after level 1.","reported_impact":"Guest-first flow = <60s time-to-first-content"},
    {"company":"Roblox","problem_solved":"D7+ retention and social habit loops","what_they_changed":"Friends activity feed, group challenges, limited-time events with leaderboards.","why_it_worked":"Social accountability and FOMO drive return visits.","applicability_to_dreamplay":"Weekly Dream Challenges (7-day events) with friends leaderboard.","reported_impact":"Limited-time events drive 2-3x session frequency vs baseline"},
]

EXPERIMENTS = [
    {"id":"EXP-01","name":"Streak Shield — Daily Play Streak","description":"Visible daily streak counter on home screen. Push notification at peak-play time if streak about to break. One-time Streak Shield power-up.","inspired_by":"Duolingo","target_metric":"Day-7 retention","hypothesis_addressed":"H1 (habit loop)","variant_split":"50/50 A/B","success_threshold":"+3pp D7 retention"},
    {"id":"EXP-02","name":"Lightning Onboarding — Win in 60 Seconds","description":"3-question quiz + guided mini-level under 60s. Delay account creation until after mini-level. Reward animation before sign-up.","inspired_by":"TikTok + Duolingo","target_metric":"Onboarding completion rate & D1 retention","hypothesis_addressed":"H1 + H2","variant_split":"50/50 A/B","success_threshold":"+5pp onboarding completion, +2pp D1 retention"},
    {"id":"EXP-03","name":"Dream Digest — Weekly Re-engagement","description":"Monday personalised push/email with Dream Stats + weekly content teaser + friends leaderboard. Deep-links into week's challenge.","inspired_by":"Spotify + Roblox","target_metric":"Day-7 and Day-14 retention","hypothesis_addressed":"H2 + H3","variant_split":"50/50 A/B","success_threshold":"+4pp D7 retention"},
    {"id":"EXP-04","name":"Smart Content Queue — Auto-next","description":"5-second countdown preview of next recommended item after content completion. Collaborative filtering; falls back to Top 10 this week.","inspired_by":"Netflix","target_metric":"Avg session time + sessions-per-user","hypothesis_addressed":"H2 (in-session engagement)","variant_split":"50/50 A/B","success_threshold":"+10% avg session time"},
]

def generate_hypotheses(problem):
    return HYPOTHESIS_BANK.get(problem.get("primary_problem",""), _FALLBACK_HYPOTHESES)

def get_benchmarks(_problem):
    return BENCHMARKS

def generate_experiments(_benchmarks, _problem):
    return EXPERIMENTS

def estimate_and_prioritise(experiments, summary, problem):
    d1 = summary["retention"]["d1_retention"]["curr"]
    d7 = summary["retention"]["d7_retention"]["curr"]
    impact_map = {
        "EXP-01": {"retention_lift":"+3-5pp D7","engagement_lift":"+15% sessions/user","reasoning":f"D7 now {d7*100:.0f}%. Duolingo streaks lifted D7 ~20% relative in comparable apps.","impact":3,"effort":2,"confidence":3},
        "EXP-02": {"retention_lift":"+2-4pp D1, +5pp onboarding","engagement_lift":"+8% S1->S2","reasoning":f"D1 now {d1*100:.0f}%. Removing friction shows 10-20% relative D1 improvement.","impact":3,"effort":2,"confidence":3},
        "EXP-03": {"retention_lift":"+3-5pp D7","engagement_lift":"+20% weekly active rate at-risk","reasoning":"Personalised weekly digests recover 15-25% of day 3-6 lapsed users.","impact":2,"effort":2,"confidence":2},
        "EXP-04": {"retention_lift":"+1-2pp D1 indirect","engagement_lift":"+10-15% avg session time","reasoning":"Netflix auto-next reduces session-end drop-off ~40%.","impact":2,"effort":3,"confidence":2},
    }
    scored = []
    for exp in experiments:
        meta = impact_map.get(exp["id"], {})
        score = (meta.get("impact",1) * meta.get("confidence",1)) / max(meta.get("effort",1),1)
        scored.append({**exp, **meta, "priority_score": round(score,2)})
    scored.sort(key=lambda x: x["priority_score"], reverse=True)
    for i,exp in enumerate(scored):
        exp["priority_rank"] = i+1
    return scored
