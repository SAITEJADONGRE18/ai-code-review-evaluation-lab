#!/usr/bin/env python3
"""Run the project's reproducible local checks using Python, Node.js, and g++."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean_stderr(stderr: str) -> str:
    # The hosted execution environment may inject an unrelated spreadsheet warmup traceback.
    marker = "Spreadsheet runtime warmup failed during python startup"
    if marker in stderr:
        stderr = stderr.split(marker, 1)[0].strip()
    return stderr.strip()


def run(name: str, command: list[str], cwd: Path = ROOT) -> dict:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=60)
    return {
        "name": name,
        "command": command,
        "return_code": result.returncode,
        "passed": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": clean_stderr(result.stderr),
    }


def main() -> int:
    checks = []
    py = sys.executable
    checks.append(run(
        "Python unit tests",
        [py, "-m", "unittest", "discover", "-s", "tests", "-v"],
    ))
    checks.append(run(
        "Benchmark evaluator unit tests",
        [py, "-m", "unittest", "test_benchmark_evaluator", "-v"],
        cwd=ROOT / "tests",
    ))
    checks.append(run(
        "Python reference cases",
        [py, "benchmarks/run_reference_tests.py"],
    ))
    checks.append(run(
        "Python candidate defect demonstrations",
        [py, "test_candidate_behaviors.py"],
        cwd=ROOT / "benchmarks",
    ))

    node = shutil.which("node")
    if node:
        js_test = r"""
const assert = require('node:assert/strict');
const {
  reverseStringCandidate, reverseStringCorrected,
  uniqueValuesCandidate, uniqueValuesCorrected
} = require('./benchmarks/javascript_candidates.js');

assert.equal(reverseStringCandidate('level'), 'level');
assert.equal(reverseStringCorrected('level'), 'level');
assert.notEqual(reverseStringCandidate('A😀B'), 'B😀A');
assert.equal(reverseStringCorrected('A😀B'), 'B😀A');
assert.deepEqual(uniqueValuesCandidate([3, 1, 3, 2, 1]), [3, 1, 2]);
assert.deepEqual(uniqueValuesCorrected([3, 1, 3, 2, 1]), [3, 1, 2]);
console.log('JavaScript candidate/corrected behavior tests passed (6 assertions)');
"""
        checks.append(run(
            "JavaScript behavior tests",
            [node, "-e", js_test],
        ))
    else:
        checks.append({
            "name": "JavaScript behavior tests",
            "command": ["node", "-e", "..."],
            "return_code": None, "passed": False,
            "stdout": "", "stderr": "Node.js not found; install Node.js to run this check.",
        })

    compiler = shutil.which("g++")
    if compiler:
        with tempfile.TemporaryDirectory(prefix="code-review-lab-") as temp:
            binary = Path(temp) / "cpp_candidates"
            checks.append(run(
                "C++ compile",
                [compiler, "-std=c++17", "-Wall", "-Wextra", "-Wpedantic",
                 str(ROOT / "benchmarks/cpp_candidates.cpp"), "-o", str(binary)],
            ))
            if checks[-1]["passed"]:
                checks.append(run("C++ corrected binary-search smoke tests", [str(binary)]))
    else:
        checks.append({
            "name": "C++ compile and smoke tests",
            "command": ["g++", "..."],
            "return_code": None, "passed": False,
            "stdout": "", "stderr": "g++ not found; install a C++17 compiler to run this check.",
        })

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    for name, command in [
        ("CLI validate", [py, "-m", "code_review_lab.cli", "validate", "examples/sample-evaluation.json"]),
        ("CLI score", [py, "-m", "code_review_lab.cli", "score", "examples/sample-evaluation.json"]),
        ("CLI A/B compare", [py, "-m", "code_review_lab.cli", "compare", "examples/sample-evaluation.json", "examples/sample-evaluation-b.json"]),
    ]:
        result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, timeout=60)
        checks.append({
            "name": name, "command": command, "return_code": result.returncode,
            "passed": result.returncode == 0, "stdout": result.stdout.strip(),
            "stderr": clean_stderr(result.stderr),
        })

    report = {
        "report_type": "local_reproducible_checks",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": "AI Code Review & Evaluation Lab",
        "note": (
            "These are local software checks on authored reference examples. "
            "They are not results from external AI models and do not establish model rankings."
        ),
        "passed": sum(1 for item in checks if item["passed"]),
        "total": len(checks),
        "all_passed": all(item["passed"] for item in checks),
        "checks": checks,
    }
    output = ROOT / "reports" / "local-checks.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for item in checks:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"[{status}] {item['name']}")
        if item["stdout"]:
            print("  " + item["stdout"].replace("\n", "\n  "))
        if item["stderr"]:
            print("  STDERR: " + item["stderr"].replace("\n", "\n  "))
    print(f"\nRESULT: {report['passed']}/{report['total']} checks passed")
    print(f"REPORT: {output.relative_to(ROOT)}")
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
