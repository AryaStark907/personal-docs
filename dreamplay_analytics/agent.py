"""
DreamPlay Autonomous Product Growth Agent
Orchestrates all 8 steps and returns a structured JSON report.

Usage:
    python agent.py
    python agent.py --project my-gcp-project --dataset dreamplay_prod
    python agent.py --output report.json
"""

from __future__ import annotations
import argparse, json, logging
from typing import Any
from bigquery_client import fetch_all
from metrics import build_metrics_summary, detect_problem
from analysis import generate_hypotheses, get_benchmarks, generate_experiments, estimate_and_prioritise

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)-8s  %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger('dreamplay.agent')

def _section(title):
    log.info('━' * 60)
    log.info('  %s', title)
    log.info('━' * 60)

def _build_recommendation(prioritised, summary, problem):
    top = prioritised[0]
    return {
        'top_experiment_id':   top['id'],
        'top_experiment_name': top['name'],
        'why_prioritised': (f"Ranked #1 (score {top['priority_score']}) due to High impact on "
                            f"'{problem['primary_problem']}', medium effort, strong benchmark "
                            f"confidence (inspired by {top['inspired_by']})."),
        'expected_business_impact': {
            'retention_lift':  top.get('retention_lift',  'N/A'),
            'engagement_lift': top.get('engagement_lift', 'N/A'),
        },
        'suggested_timeline':   '2-week sprint to ship A/B test; 2-week measurement window',
        'secondary_experiment': prioritised[1]['id'] if len(prioritised) > 1 else None,
        'key_risk': ('Push-notification dependency in EXP-01 requires adequate opt-in rate. '
                     'Pair with EXP-02 to ensure permission is requested at the right moment.'),
    }

def run_pipeline(project, dataset):
    _section('STEP 0 — Connecting to BigQuery')
    raw = fetch_all(project=project, dataset=dataset)
    log.info('Data source: %s', raw['source'])
    _section('STEP 1 — Aggregating metrics')
    summary = build_metrics_summary(raw)
    _section('STEP 2 — Detecting primary problem')
    problem = detect_problem(summary)
    log.info('Primary problem : %s (%s WoW)', problem['primary_problem'], problem['wow_change'])
    log.info('Affected stage  : %s', problem['affected_stage'])
    _section('STEP 3 — Generating root-cause hypotheses')
    hypotheses = generate_hypotheses(problem)
    for h in hypotheses:
        log.info('[%s] (%s) %s', h['id'], h['likelihood'], h['hypothesis'])
    _section('STEP 4 — External benchmarking')
    benchmarks = get_benchmarks(problem)
    for b in benchmarks:
        log.info('%s → %s', b['company'], b['reported_impact'])
    _section('STEP 5 — Generating experiments')
    experiments = generate_experiments(benchmarks, problem)
    for e in experiments:
        log.info('[%s] %s (target: %s)', e['id'], e['name'], e['target_metric'])
    _section('STEP 6 & 7 — Impact estimation and prioritisation')
    prioritised = estimate_and_prioritise(experiments, summary, problem)
    for e in prioritised:
        log.info('Rank %d  [%s]  %s  score=%.2f', e['priority_rank'], e['id'], e['name'], e['priority_score'])
    _section('STEP 8 — Final recommendation')
    recommendation = _build_recommendation(prioritised, summary, problem)
    log.info('→ %s', recommendation['top_experiment_name'])
    log.info('  %s', recommendation['why_prioritised'])
    return {
        'metrics_summary': summary,
        'problem':         problem['description'],
        'root_causes':     hypotheses,
        'benchmarks':      benchmarks,
        'experiments':     prioritised,
        'recommendation':  recommendation,
    }

def main():
    parser = argparse.ArgumentParser(description='DreamPlay Product Growth Agent')
    parser.add_argument('--project', default='YOUR_PROJECT_ID')
    parser.add_argument('--dataset', default='YOUR_DATASET')
    parser.add_argument('--output',  default=None)
    args = parser.parse_args()
    report = run_pipeline(project=args.project, dataset=args.dataset)
    json_output = json.dumps(report, indent=2, default=str)
    if args.output:
        with open(args.output, 'w') as fh:
            fh.write(json_output)
        log.info('Report written to %s', args.output)
    else:
        print(json_output)

if __name__ == '__main__':
    main()
