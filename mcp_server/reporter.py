"""
Results Reporter

Generates and manages test results, reports, and artifacts.
Supports JSON and Markdown output formats.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from jinja2 import Template

logger = logging.getLogger(__name__)


class ResultReporter:
    """Manages test results and generates reports"""

    def __init__(self, results_dir: str = "results", logs_dir: str = "logs"):
        self.results_dir = Path(results_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def create_report(
        self,
        run_id: str,
        scenario: Any,
        code: str,
        execution_result: Dict[str, Any],
        evaluation: Dict[str, Any],
        explanation: str = ""
    ) -> Dict[str, Any]:
        """Create a comprehensive test report"""

        report = {
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "scenario": {
                "id": scenario.id,
                "title": scenario.title,
                "category": scenario.category,
                "difficulty": scenario.difficulty,
                "description": scenario.description
            },
            "submission": {
                "code": code,
                "language": scenario.language,
                "explanation": explanation,
                "code_length": len(code),
                "lines_of_code": len(code.split('\n'))
            },
            "execution": {
                "success": execution_result.get("success", False),
                "output": execution_result.get("output", ""),
                "errors": execution_result.get("errors", ""),
                "return_code": execution_result.get("return_code"),
                "test_results": execution_result.get("test_results", []),
                "environment": execution_result.get("execution_environment", "subprocess")
            },
            "evaluation": evaluation,
            "metadata": {
                "server_version": "1.0.0",
                "evaluation_engine": "deepeval" if evaluation.get("metrics", {}).get("deepeval") else "basic"
            }
        }

        return report

    def save_results(self, run_id: str, report: Dict[str, Any]):
        """Save results to JSON file"""
        # Save JSON
        json_path = self.results_dir / f"{run_id}.json"
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Results saved to {json_path}")

        # Save Markdown report
        md_path = self.results_dir / f"{run_id}.md"
        markdown = self._generate_markdown_report(report)
        md_path.write_text(markdown)

        logger.info(f"Markdown report saved to {md_path}")

        # Save code snapshot
        code_path = self.results_dir / f"{run_id}_code.{report['submission']['language']}"
        code_path.write_text(report['submission']['code'])

    def load_results(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Load results from JSON file"""
        json_path = self.results_dir / f"{run_id}.json"

        if not json_path.exists():
            return None

        with open(json_path, 'r') as f:
            return json.load(f)

    def list_runs(
        self,
        scenario_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all test runs with optional filtering"""
        runs = []

        for json_file in self.results_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    report = json.load(f)

                # Apply filters
                if scenario_id and report["scenario"]["id"] != scenario_id:
                    continue

                if status and report["evaluation"]["status"] != status:
                    continue

                # Create summary
                runs.append({
                    "run_id": report["run_id"],
                    "timestamp": report["timestamp"],
                    "scenario_id": report["scenario"]["id"],
                    "scenario_title": report["scenario"]["title"],
                    "status": report["evaluation"]["status"],
                    "score": report["evaluation"]["overall_score"],
                    "passed": report["evaluation"]["passed"]
                })

            except Exception as e:
                logger.warning(f"Error loading {json_file}: {e}")

        # Sort by timestamp (newest first)
        runs.sort(key=lambda x: x["timestamp"], reverse=True)

        return runs

    def _generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate Markdown report"""

        template = Template('''# Test Report: {{ report.scenario.title }}

**Run ID:** `{{ report.run_id }}`
**Timestamp:** {{ report.timestamp }}
**Status:** {{ "✓ PASSED" if report.evaluation.passed else "✗ FAILED" }}
**Score:** {{ report.evaluation.overall_score }}/1.00

---

## Scenario Details

**ID:** {{ report.scenario.id }}
**Category:** {{ report.scenario.category }}
**Difficulty:** {{ report.scenario.difficulty }}

**Description:**
{{ report.scenario.description }}

---

## Submission

**Language:** {{ report.submission.language }}
**Code Length:** {{ report.submission.code_length }} characters ({{ report.submission.lines_of_code }} lines)

{% if report.submission.explanation %}
**Explanation:**
{{ report.submission.explanation }}
{% endif %}

**Code:**
```{{ report.submission.language }}
{{ report.submission.code }}
```

---

## Execution Results

**Success:** {{ "Yes" if report.execution.success else "No" }}
**Return Code:** {{ report.execution.return_code }}
**Environment:** {{ report.execution.environment }}

{% if report.execution.output %}
**Output:**
```
{{ report.execution.output }}
```
{% endif %}

{% if report.execution.errors %}
**Errors:**
```
{{ report.execution.errors }}
```
{% endif %}

{% if report.execution.test_results %}
### Test Cases

| Test | Status | Description |
|------|--------|-------------|
{% for test in report.execution.test_results %}
| {{ test.test_case }} | {{ "✓ PASS" if test.passed else "✗ FAIL" }} | {{ test.get('description', 'N/A') }} |
{% endfor %}
{% endif %}

---

## Evaluation

**Overall Score:** {{ report.evaluation.overall_score }}/1.00
**Status:** {{ report.evaluation.status }}

### Metrics

{% for metric_name, metric_data in report.evaluation.metrics.items() %}
#### {{ metric_name.title() }}
- **Score:** {{ metric_data.score }}/1.00
- **Details:** {{ metric_data.details }}
{% if metric_data.get('issues') %}
- **Issues:** {{ metric_data.issues | join(', ') }}
{% endif %}
{% endfor %}

### Feedback

{% for item in report.evaluation.feedback %}
- {{ item }}
{% endfor %}

### Summary

{{ report.evaluation.summary }}

---

*Generated by Agent Testing MCP Server v{{ report.metadata.server_version }}*
''')

        return template.render(report=report)

    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate summary statistics across all test runs"""
        all_runs = self.list_runs()

        if not all_runs:
            return {
                "total_runs": 0,
                "message": "No test runs found"
            }

        total = len(all_runs)
        passed = sum(1 for r in all_runs if r["passed"])
        failed = total - passed

        # Calculate average score
        avg_score = sum(r["score"] for r in all_runs) / total if total > 0 else 0

        # Group by scenario
        by_scenario = {}
        for run in all_runs:
            sid = run["scenario_id"]
            if sid not in by_scenario:
                by_scenario[sid] = {
                    "scenario_id": sid,
                    "scenario_title": run["scenario_title"],
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "avg_score": 0
                }

            by_scenario[sid]["total"] += 1
            if run["passed"]:
                by_scenario[sid]["passed"] += 1
            else:
                by_scenario[sid]["failed"] += 1

        # Calculate averages
        for scenario_stats in by_scenario.values():
            scenario_runs = [r for r in all_runs if r["scenario_id"] == scenario_stats["scenario_id"]]
            scenario_stats["avg_score"] = sum(r["score"] for r in scenario_runs) / len(scenario_runs)

        return {
            "total_runs": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / total * 100, 1) if total > 0 else 0,
            "average_score": round(avg_score, 2),
            "by_scenario": list(by_scenario.values()),
            "recent_runs": all_runs[:10]  # Last 10 runs
        }
