"""Print a pass/skip/fail summary of the JUnit XML reports in reports/.

Used by the GitHub Actions workflow. Blocked tests are skipped (not failed), so a
green run can still mean "nothing was verified" - this makes that visible.
"""
import glob
import os
import xml.etree.ElementTree as ET


def read_suite(path):
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    tests = int(suite.get("tests", 0))
    skipped = int(suite.get("skipped", 0))
    failed = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
    return tests, tests - skipped - failed, skipped, failed


def main():
    lines = ["## Test summary", "", "| Group | Passed | Skipped | Failed |", "|---|---|---|---|"]
    total = passed = skipped = failed = 0
    for path in sorted(glob.glob("reports/*.xml")):
        group = os.path.splitext(os.path.basename(path))[0]
        t, p, s, f = read_suite(path)
        total, passed, skipped, failed = total + t, passed + p, skipped + s, failed + f
        lines.append(f"| {group} | {p} | {s} | {f} |")
    lines.append(f"| **Total** | **{passed}** | **{skipped}** | **{failed}** |")
    if skipped:
        lines += [
            "",
            f"> **{skipped} of {total} tests were skipped** - the site's bot protection blocks "
            "GitHub's servers, so this run did NOT verify them. Run locally for a full result (see README).",
        ]
    text = "\n".join(lines)
    print(text)

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as fh:
            fh.write(text + "\n")
    if skipped:
        print(f"::warning::{skipped} of {total} tests were skipped (blocked by the site). Run locally for a full result.")


if __name__ == "__main__":
    main()
