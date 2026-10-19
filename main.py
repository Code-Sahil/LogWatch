
import argparse
import json
import re
from collections import Counter
from pathlib import Path

LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\]\s+"
    r"(?P<level>INFO|DEBUG|WARNING|ERROR|CRITICAL)\s+"
    r"(?P<message>.+)$",
    re.IGNORECASE,
)

FAILURE_LEVELS = {"ERROR", "CRITICAL"}


def analyze_log(log_path, alert_threshold=3):
    counts = Counter()
    total_lines = 0
    valid_lines = 0
    malformed_lines = 0

    with open(log_path, "r", encoding="utf-8") as file:
        for line in file:
            total_lines += 1
            line = line.strip()

            if not line:
                continue

            match = LOG_PATTERN.match(line)

            if not match:
                malformed_lines += 1
                continue

            level = match.group("level").upper()
            counts[level] += 1
            valid_lines += 1

    failures = sum(counts[level] for level in FAILURE_LEVELS)

    failure_rate = (
        round(failures / valid_lines * 100, 2)
        if valid_lines
        else 0.0
    )

    alerts = []

    if counts["CRITICAL"] > 0:
        alerts.append("Critical failures detected")

    if failures >= alert_threshold:
        alerts.append(
            f"Failure threshold exceeded: "
            f"{failures} failures (threshold: {alert_threshold})"
        )

    return {
        "source": str(log_path),
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "malformed_lines": malformed_lines,
        "counts_by_level": dict(sorted(counts.items())),
        "failure_count": failures,
        "failure_rate_percent": failure_rate,
        "alerts": alerts,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze application logs and detect failures."
    )
    parser.add_argument(
        "--input", default="logs/app.log",
        help="Path to the input log file",
    )
    parser.add_argument(
        "--output", default="reports/report.json",
        help="Path to the JSON report",
    )
    parser.add_argument(
        "--threshold", type=int, default=3,
        help="Number of failures required to trigger an alert",
    )
    args = parser.parse_args()

    if args.threshold < 1:
        parser.error("--threshold must be at least 1")

    log_path = Path(args.input)
    report_path = Path(args.output)

    if not log_path.is_file():
        parser.error(f"Input log file not found: {log_path}")

    report = analyze_log(log_path, args.threshold)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()

