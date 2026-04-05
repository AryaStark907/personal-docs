"""
BigQuery client wrapper for DreamPlay analytics.
Falls back to mock data when credentials are unavailable.
"""

import os
import logging
from datetime import date, timedelta
from typing import Any

logger = logging.getLogger(__name__)

CORE_METRICS_SQL = """
SELECT
  DATE(date)                             AS date,
  COUNT(DISTINCT user_id)                AS dau,
  AVG(session_time)                      AS avg_session_time,
  SUM(session_count)                     AS total_sessions
FROM `{project}.{dataset}.session_logs`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
GROUP BY date
ORDER BY date
"""

RETENTION_SQL = """
WITH cohort AS (
  SELECT user_id, MIN(DATE(event_time)) AS first_day
  FROM `{project}.{dataset}.funnel_events`
  WHERE event_name = 'session_start'
  GROUP BY user_id
),
activity AS (
  SELECT DISTINCT user_id, DATE(event_time) AS active_day
  FROM `{project}.{dataset}.funnel_events`
  WHERE event_name = 'session_start'
)
SELECT
  c.first_day AS cohort_date,
  DATE_DIFF(a.active_day, c.first_day, DAY) AS day_number,
  COUNT(DISTINCT c.user_id) AS cohort_size,
  COUNT(DISTINCT a.user_id) AS retained_users
FROM cohort c
JOIN activity a USING (user_id)
WHERE c.first_day >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
  AND DATE_DIFF(a.active_day, c.first_day, DAY) IN (1, 7)
GROUP BY cohort_date, day_number
ORDER BY cohort_date, day_number
"""

FUNNEL_SQL = """
SELECT
  event_name,
  COUNT(DISTINCT user_id) AS users,
  COUNT(*) AS events
FROM `{project}.{dataset}.funnel_events`
WHERE DATE(event_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND event_name IN ('onboarding_start','onboarding_complete','session_start','session_2_start')
GROUP BY event_name
ORDER BY users DESC
"""

SESSION_DEPTH_SQL = """
SELECT
  session_number,
  COUNT(DISTINCT user_id) AS users
FROM `{project}.{dataset}.user_metrics_daily`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND session_number <= 10
GROUP BY session_number
ORDER BY session_number
"""

def _mock_daily_metrics():
    base = date.today() - timedelta(days=14)
    dau_trend    = [1800,1850,1820,1900,1780,1760,1840,1650,1620,1580,1600,1540,1510,1530]
    session_time = [420,415,422,418,410,408,425,390,385,378,380,372,368,375]
    sessions     = [3.1,3.2,3.1,3.3,3.0,3.0,3.2,2.8,2.7,2.7,2.8,2.6,2.5,2.6]
    return [{"date": (base+timedelta(days=i)).isoformat(), "dau": dau_trend[i],
             "avg_session_time": session_time[i], "total_sessions": sessions[i]} for i in range(14)]

def _mock_retention():
    return [
        {"period": "prev_week", "day_number": 1, "retention_rate": 0.42},
        {"period": "prev_week", "day_number": 7, "retention_rate": 0.18},
        {"period": "curr_week", "day_number": 1, "retention_rate": 0.36},
        {"period": "curr_week", "day_number": 7, "retention_rate": 0.14},
    ]

def _mock_funnel():
    return [
        {"event_name": "onboarding_start",    "users": 5200},
        {"event_name": "onboarding_complete", "users": 3380},
        {"event_name": "session_start",       "users": 3200},
        {"event_name": "session_2_start",     "users": 1600},
    ]

def _mock_session_depth():
    counts = [3200,1600,960,640,450,330,250,200,160,130]
    return [{"session_number": i+1, "users": c} for i,c in enumerate(counts)]

def fetch_all(project="YOUR_PROJECT_ID", dataset="YOUR_DATASET"):
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=project)
        logger.info("BigQuery client initialised — querying live data.")
        def run(sql):
            return [dict(row) for row in client.query(sql.format(project=project, dataset=dataset)).result()]
        return {"daily_metrics": run(CORE_METRICS_SQL), "retention": run(RETENTION_SQL),
                "funnel": run(FUNNEL_SQL), "session_depth": run(SESSION_DEPTH_SQL), "source": "bigquery"}
    except Exception as exc:
        logger.warning("BigQuery unavailable (%s) — using mock data.", exc)
        return {"daily_metrics": _mock_daily_metrics(), "retention": _mock_retention(),
                "funnel": _mock_funnel(), "session_depth": _mock_session_depth(), "source": "mock"}
