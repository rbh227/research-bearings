#!/usr/bin/env bash
# Assemble the wildfire fixture shape into this run's empty workspace. Runs only
# under `claude plugin eval --scaffold`; see evals/fixtures/README.md.
set -euo pipefail
"$(cd "$(dirname "${BASH_SOURCE[0]}")/../fixtures" && pwd)/assemble.sh" wildfire "$PWD/research"
