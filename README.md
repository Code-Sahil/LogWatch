# LogWatch

A lightweight, rule-based log analysis and alerting tool built with Python, Docker, and GitHub Actions.

## Features

- Parse application logs with timestamps and severity levels.
- Count log events by severity.
- Calculate failure counts and failure rates.
- Detect critical events and configurable failure thresholds.
- Generate machine-readable JSON reports.
- Run as a Docker container.
- Execute automated unit tests through GitHub Actions.

## Project Structure

```text
LogWatch/
├── .github/
│   └── workflows/
│       └── tests.yml
├── logs/
│   └── app.log
├── reports/
├── Dockerfile
├── main.py
├── test_main.py
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 or compatible Python version
- Docker Desktop (for container execution)
- Git (for version control)

## Run Locally

Clone the repository:

```bash
git clone https://github.com/Code-Sahil/LogWatch.git
cd LogWatch
```

Run the analyzer:

```bash
python main.py
```

The default input file is `logs/app.log`. The JSON report is written to `reports/report.json`.

## Configuration

Specify a different failure threshold:

```bash
python main.py --threshold 5
```

Specify custom input and output paths:

```bash
python main.py --input logs/app.log --output reports/custom-report.json
```

View all command-line options:

```bash
python main.py --help
```

## Run Tests

Execute the automated test suite:

```bash
python -m unittest -v
```

GitHub Actions runs the tests automatically on pushes and pull requests.

## Run with Docker

Build the image:

```bash
docker build -t logwatch:1.0 .
```

Run LogWatch with mounted input and output directories in PowerShell:

```powershell
docker run --rm `
  -v "${PWD}/logs:/app/logs:ro" `
  -v "${PWD}/reports:/app/reports" `
  logwatch:1.0
```

Run with a custom failure threshold:

```powershell
docker run --rm `
  -v "${PWD}/logs:/app/logs:ro" `
  -v "${PWD}/reports:/app/reports" `
  logwatch:1.0 `
  --threshold 5
```

The input directory is mounted read-only, and generated reports persist in the host's `reports` directory.

## Alerting Rules

- A critical event triggers a critical-failure alert.
- The failure threshold triggers an alert when the number of `ERROR` and `CRITICAL` entries meets or exceeds the configured threshold.
- The failure rate is calculated as the percentage of valid log entries classified as `ERROR` or `CRITICAL`.

## Current Limitations

- Processes a log file in batch mode rather than continuously monitoring it.
- Uses rule-based detection rather than anomaly detection.
- Does not yet send external notifications.
- The current CI workflow runs unit tests but does not build the Docker image.

## Future Improvements

- Support multiple log files.
- Add continuous log monitoring.
- Introduce configurable severity rules.
- Add structured logging and richer error handling.
- Test Docker builds automatically in CI.
- Add notification integrations and operational metrics.

## License

No license has been added yet. Reuse and redistribution permissions should be defined before the project is distributed publicly.