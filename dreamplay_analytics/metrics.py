"""
STEP 1 & 2 — Data aggregation, trend analysis, problem detection.
"""

from __future__ import annotations
import statistics
from typing import Any


def _pct_change(old: float, new: float) -> float:
    if old == 0:
        return 0.0
    return round((new - old) / old * 100, 2)


def _week_split(rows):
    return rows[:7], rows[7:]


def aggregate_daily(daily_metrics):
    prev, curr = _week_split(daily_metrics)
    def avg(rows, key):
        return statistics.mean(r[key] for r in rows)
    prev_dau  = avg(prev, "dau");  curr_dau  = avg(curr, "dau")
    prev_time = avg(prev, "avg_session_time"); curr_time = avg(curr, "avg_session_time")
    prev_sess = avg(prev, "total_sessions");   curr_sess = avg(curr, "total_sessions")
    return {
        "prev_week": {"avg_dau": round(prev_dau,1), "avg_session_time": round(prev_time,1), "avg_sessions": round(prev_sess,2)},
        "curr_week": {"avg_dau": round(curr_dau,1), "avg_session_time": round(curr_time,1), "avg_sessions": round(curr_sess,2)},
        "wow_changes": {"dau_pct": _pct_change(prev_dau,curr_dau), "session_time_pct": _pct_change(prev_time,curr_time), "sessions_pct": _pct_change(prev_sess,curr_sess)},
    }


def aggregate_retention(retention):
    def get(period, day):
        for r in retention:
            if r["period"] == period and r["day_number"] == day:
                return r["retention_rate"]
        return 0.0
    d1_prev=get("prev_week",1); d1_curr=get("curr_week",1)
    d7_prev=get("prev_week",7); d7_curr=get("curr_week",7)
    return {
        "d1_retention": {"prev": d1_prev, "curr": d1_curr, "wow_pct": _pct_change(d1_prev,d1_curr)},
        "d7_retention": {"prev": d7_prev, "curr": d7_curr, "wow_pct": _pct_change(d7_prev,d7_curr)},
    }


def aggregate_funnel(funnel):
    users = {r["event_name"]: r["users"] for r in funnel}
    ob_start    = users.get("onboarding_start", 1)
    ob_complete = users.get("onboarding_complete", 0)
    s1 = users.get("session_start", 0)
    s2 = users.get("session_2_start", 0)
    return {
        "onboarding_completion_rate": round(ob_complete/ob_start*100,1) if ob_start else 0,
        "session_1_to_2_rate":        round(s2/s1*100,1) if s1 else 0,
        "raw_counts": users,
    }


def build_metrics_summary(raw):
    return {
        "data_source": raw.get("source","unknown"),
        "daily":       aggregate_daily(raw["daily_metrics"]),
        "retention":   aggregate_retention(raw["retention"]),
        "funnel":      aggregate_funnel(raw["funnel"]),
    }


def detect_problem(summary):
    wow = summary["daily"]["wow_changes"]
    ret = summary["retention"]
    fun = summary["funnel"]
    candidates = [
        {"metric": "Day-1 Retention", "change": ret["d1_retention"]["wow_pct"], "current": f"{ret['d1_retention']['curr']*100:.1f}%", "stage": "Early retention / onboarding"},
        {"metric": "Day-7 Retention", "change": ret["d7_retention"]["wow_pct"], "current": f"{ret['d7_retention']['curr']*100:.1f}%", "stage": "Habit formation"},
        {"metric": "DAU",             "change": wow["dau_pct"],                 "current": str(summary["daily"]["curr_week"]["avg_dau"]), "stage": "Acquisition / top-of-funnel"},
        {"metric": "Avg Session Time","change": wow["session_time_pct"],        "current": f"{summary['daily']['curr_week']['avg_session_time']}s", "stage": "In-session engagement"},
        {"metric": "Session 1→2 Conversion", "change": 0.0,                    "current": f"{fun['session_1_to_2_rate']}%", "stage": "Early activation"},
    ]
    worst = min(candidates, key=lambda c: c["change"])
    return {
        "primary_problem": worst["metric"],
        "wow_change":      f"{worst['change']}%",
        "current_value":   worst["current"],
        "affected_stage":  worst["stage"],
        "description":     f"{worst['metric']} dropped {abs(worst['change']):.1f}% WoW (now {worst['current']}), indicating weakening at the '{worst['stage']}' stage.",
    }
