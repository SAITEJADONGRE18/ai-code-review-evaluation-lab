# Reference examples and local test runners

These files are deliberately small examples for demonstrating the evaluation method. They are not attributed to a specific AI model.

## Python

From the `benchmarks` directory:

```bash
python run_reference_tests.py
```

This runner executes tests against the corrected Python implementations. It does not execute unsafe candidate implementations.

## JavaScript

With Node.js installed, from the repository root:

```bash
node -e "const x=require('./benchmarks/javascript_candidates'); console.log(x.reverseStringCorrected('A😀B')); console.log(x.uniqueValuesCorrected([1,2,1,3]))"
```

Expected output includes `B😀A` and `[1, 2, 3]`. Run additional tests before recording results in an evaluation report.

## C++

With a C++17 compiler:

```bash
cd benchmarks
g++ -std=c++17 -Wall -Wextra -Wpedantic cpp_candidates.cpp -o cpp_candidates
./cpp_candidates
```

Where supported, add `-fsanitize=address,undefined` during development. The C++ source includes only corrected-code smoke tests; the unsafe candidate is documented, not invoked on boundary inputs.

## Run all local checks

From the repository root:

```bash
python benchmarks/run_all_checks.py
```

The runner checks the Python unit/reference tests, JavaScript candidate and corrected behavior,
C++ compilation/smoke tests (when `g++` is installed), and all three CLI commands. It writes
`reports/local-checks.json` with command output and pass/fail status. Install Node.js and a
C++17 compiler to run every language check.

**Provenance:** candidate and corrected implementations in this repository are authored teaching
examples designed to demonstrate review scenarios. They are not represented as outputs from
specific commercial AI models. Consequently, the included score comparisons demonstrate the
tooling only; they are not a scientific model leaderboard.

