"""Offline validation and score calculation for human-reviewed grade reports.

Not an AI model, not connected to Google Drive, and not connected to GoHighLevel.
"""
import json
import sys
from pathlib import Path


class GradingError(ValueError):
    pass


def calculate(report: dict, rubric: dict) -> dict:
    if report.get("rubric_id") != rubric.get("rubric_id"):
        raise GradingError("Rubric ID mismatch")
    if report.get("rubric_version") != rubric.get("version"):
        raise GradingError("Rubric version mismatch")
    criteria = rubric["criteria"]
    rubric_by_id = {item["id"]: item for item in criteria}
    if len(rubric_by_id) != len(criteria):
        raise GradingError("Duplicate criterion IDs in rubric")
    grades = report.get("criteria_scores", [])
    if {item.get("criterion_id") for item in grades} != set(rubric_by_id) or len(grades) != len(rubric_by_id):
        raise GradingError("Missing, unexpected or duplicated criterion")
    score = 0
    for item in grades:
        criterion = rubric_by_id[item["criterion_id"]]
        points = item.get("points")
        if type(points) is not int or not 0 <= points <= criterion["max_points"]:
            raise GradingError(f"Invalid score for {criterion['id']}")
        if not str(item.get("justification", "")).strip():
            raise GradingError(f"Missing justification for {criterion['id']}")
        if not item.get("evidence_refs"):
            raise GradingError(f"Missing evidence references for {criterion['id']}")
        score += points
    total = rubric["total_points"]
    if sum(c["max_points"] for c in criteria) != total or total <= 0:
        raise GradingError("Invalid rubric total")
    status = report.get("status")
    if status in {"approved", "released"} and not (report.get("approved_by") and report.get("approved_at")):
        raise GradingError("Instructor approval required")
    if status == "released" and not report.get("released_at"):
        raise GradingError("Release timestamp required")
    if status not in {"approved", "released"} and report.get("released_at"):
        raise GradingError("Cannot release unapproved report")
    if status == "pending_instructor_review" and (report.get("approved_by") or report.get("approved_at")):
        raise GradingError("Draft cannot contain approval metadata")
    return {"earned": score, "possible": total, "percentage": round(score / total * 100, 2),
            "meets_provisional_threshold": score >= rubric["passing_points_provisional"],
            "status": status, "release_authorized": status in {"approved", "released"},
            "warning": "Provisional threshold only; no automatic certification or notification."}


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.grader REPORT.json RUBRIC.json", file=sys.stderr)
        return 2
    try:
        report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        rubric = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        print(json.dumps(calculate(report, rubric), indent=2))
    except (OSError, json.JSONDecodeError, GradingError, KeyError, TypeError) as exc:
        print(f"Grading error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
