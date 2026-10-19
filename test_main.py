
import tempfile
import unittest
from pathlib import Path

from main import analyze_log


class TestLogWatch(unittest.TestCase):

    def analyze_text(self, text):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "test.log"
            log_path.write_text(text, encoding="utf-8")
            return analyze_log(log_path)

    def test_counts_log_levels(self):
        report = self.analyze_text(
            "[2026-10-19 10:00:00] INFO Started\n"
            "[2026-10-19 10:00:01] ERROR Failed\n"
        )

        self.assertEqual(report["valid_lines"], 2)
        self.assertEqual(report["failure_count"], 1)
        self.assertEqual(
            report["counts_by_level"]["INFO"], 1
        )

    def test_critical_event_triggers_alert(self):
        report = self.analyze_text(
            "[2026-10-19 10:00:00] CRITICAL System failure\n"
        )

        self.assertTrue(
            any("Critical" in alert for alert in report["alerts"])
        )

    def test_malformed_line_is_detected(self):
        report = self.analyze_text("This is not a valid log entry\n")

        self.assertEqual(report["valid_lines"], 0)
        self.assertEqual(report["malformed_lines"], 1)

    def test_empty_file(self):
        report = self.analyze_text("")

        self.assertEqual(report["valid_lines"], 0)
        self.assertEqual(report["failure_rate_percent"], 0.0)

    
    def test_failure_threshold_triggers_alert(self):
        report = self.analyze_text(
            "[2026-10-19 10:00:00] ERROR Failure one\n"
            "[2026-10-19 10:00:01] ERROR Failure two\n"
            "[2026-10-19 10:00:02] ERROR Failure three\n"
        )

        self.assertEqual(report["failure_count"], 3)
        self.assertTrue(
            any("threshold exceeded" in alert.lower()
                for alert in report["alerts"])
        )

    def test_blank_lines_are_not_malformed(self):
        report = self.analyze_text(
            "[2026-10-19 10:00:00] INFO Started\n"
            "\n"
            "   \n"
        )

        self.assertEqual(report["total_lines"], 3)
        self.assertEqual(report["valid_lines"], 1)
        self.assertEqual(report["malformed_lines"], 0)

    def test_mixed_valid_and_malformed_lines(self):
        report = self.analyze_text(
            "[2026-10-19 10:00:00] INFO Started\n"
            "This line is invalid\n"
            "[2026-10-19 10:00:02] ERROR Failure\n"
        )

        self.assertEqual(report["total_lines"], 3)
        self.assertEqual(report["valid_lines"], 2)
        self.assertEqual(report["malformed_lines"], 1)
        self.assertEqual(report["failure_count"], 1)



if __name__ == "__main__":
    unittest.main()
