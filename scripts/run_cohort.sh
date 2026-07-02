#!/usr/bin/env bash
# Generate a prostate cohort with the custom Synthea module.
#
# Usage: scripts/run_cohort.sh [population] [ageRange] [gender] [state]
# Defaults: 100 males aged 50-60 (US demographics for now; EU localization TBD).
#
# Loads modules/adult/prostate.json via Synthea's -d (local module dir) flag.
# Output (FHIR R4 bundles) lands in synthea/output/ (gitignored).
set -euo pipefail

POP="${1:-100}"
AGE="${2:-50-60}"
GENDER="${3:-M}"
STATE="${4:-Massachusetts}"

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SYNTHEA="$REPO/synthea"
# NOTE: Synthea treats files in SUBDIRECTORIES of the -d dir as *submodules*
# (only run when CALLED via CallSubmodule). Top-level modules must sit directly
# in the -d dir. So we point -d at modules/adult, where prostate.json lives flat.
MODULES="${MODULE_DIR:-$REPO/modules/adult}"

if [ ! -x "$SYNTHEA/run_synthea" ]; then
  echo "Synthea not found at $SYNTHEA (clone it first: git clone https://github.com/synthetichealth/synthea)" >&2
  exit 1
fi

echo "Generating $POP patients | age $AGE | gender $GENDER | $STATE | modules: $MODULES"
cd "$SYNTHEA"
./run_synthea -p "$POP" -a "$AGE" -g "$GENDER" -d "$MODULES" "$STATE"
echo "Done. Bundles in $SYNTHEA/output/fhir/"
