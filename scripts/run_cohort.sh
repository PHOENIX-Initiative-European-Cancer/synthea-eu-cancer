#!/usr/bin/env bash
# Generate a prostate cohort with the custom Synthea module.
#
# Usage: scripts/run_cohort.sh [population] [ageRange] [gender] [state]
# Defaults: 100 males aged 50-60 (US demographics for now; EU localization TBD).
#
# Reproducibility: SEED and CLINICIAN_SEED are pinned (default 42) so a run is
# bit-for-bit reproducible given the same Synthea version + module version. Set
# SEED=random (or any other value) to draw a fresh cohort. For identical patient
# TIMELINES across different days, also pin REFERENCE_DATE (Synthea ages people
# relative to it; unset = today), e.g. REFERENCE_DATE=20260701.
#
# Loads modules/adult/prostate.json via Synthea's -d (local module dir) flag.
# Output (FHIR R4 bundles) lands in synthea/output/ (gitignored).
set -euo pipefail

POP="${1:-100}"
AGE="${2:-50-60}"
GENDER="${3:-M}"
STATE="${4:-Massachusetts}"

# Reproducibility knobs (override via env). Default: fixed seed 42.
SEED="${SEED:-42}"
CLINICIAN_SEED="${CLINICIAN_SEED:-42}"
REFERENCE_DATE="${REFERENCE_DATE:-}"
# NOTE (2026-09-08): the module's 2018-2022 year window (Year_Lottery) is
# currently DISABLED (Age_50_Guard bypasses it; team decision - the window
# includes the COVID slowdown and pins the dataset to 2022). All patients use
# the 5-yr-average waiting times; REFERENCE_DATE has no special constraint.
# If the window is re-enabled in prostate.json, set REFERENCE_DATE=20221231
# (see docs/time_variance.md).

# On Windows/Git-Bash, java (via gradlew) and the python3 launcher mangle
# POSIX-style paths (e.g. /c/Users/..) passed as arguments into "C:\c\Users\.."
# instead of "C:\Users\..". Convert to forward-slash Windows paths before
# handing them to those non-bash executables (falls back to the original path
# where cygpath is unavailable, e.g. macOS/Linux).
winpath() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1"; }

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

# Build reproducibility flags. SEED=random -> omit -s so Synthea seeds from the clock.
SEED_FLAGS=()
if [ "$SEED" != "random" ]; then
  SEED_FLAGS+=(-s "$SEED" -cs "$CLINICIAN_SEED")
fi
if [ -n "$REFERENCE_DATE" ]; then
  SEED_FLAGS+=(-r "$REFERENCE_DATE")
fi

echo "Generating $POP patients | age $AGE | gender $GENDER | $STATE | modules: $MODULES"
echo "Reproducibility: seed=$SEED clinicianSeed=$CLINICIAN_SEED referenceDate=${REFERENCE_DATE:-<today>}"
cd "$SYNTHEA"
# --exporter.fhir.use_us_core_ig=false: EU dataset - do not stamp US-Core meta.profile
# claims on every resource (they drag US-Core conformance checks into ECCDM validation).
./run_synthea "${SEED_FLAGS[@]}" -p "$POP" -a "$AGE" -g "$GENDER" -d "$(winpath "$MODULES")" \
  --exporter.fhir.use_us_core_ig=false "$STATE"
echo "Done. Bundles in $SYNTHEA/output/fhir/"

# --- post-processing: restore codings Synthea's exporter drops ---------------
# Synthea keeps only the FIRST coding per medication, so the module's German
# BfArM/ATC-DE coding is lost on export. Re-add it so the data is truly dual-ATC.
echo "Post-processing: dual ATC (WHO + BfArM/ATC-DE)"
python3 "$(winpath "$REPO/scripts/postprocess_atc_de.py")" "$(winpath "$SYNTHEA/output/fhir")"
echo "Post-processing: synthetic-data tag (SYNDERAI convention) on every resource"
python3 "$(winpath "$REPO/scripts/postprocess_synthetic_tag.py")" "$(winpath "$SYNTHEA/output/fhir")"
echo "Post-processing: ECCDM layer (HL7-EU Cancer Common draft profiles)"
python3 "$(winpath "$REPO/scripts/postprocess_ccdm.py")" "$(winpath "$SYNTHEA/output/fhir")"

# --- provenance: document exactly how this cohort was produced -------------
FHIR_DIR="$SYNTHEA/output/fhir"
PROV_DIR="$REPO/provenance"
mkdir -p "$PROV_DIR"

RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_ID="run_seed${SEED}_${RUN_TS}"
MODULE_FILE="$MODULES/prostate.json"

# generator + module provenance (with fallbacks if git/tools are absent)
SYNTHEA_VER="$(git -C "$SYNTHEA" describe --tags --always 2>/dev/null || echo unknown)"
SYNTHEA_COMMIT="$(git -C "$SYNTHEA" rev-parse HEAD 2>/dev/null || echo unknown)"
REPO_COMMIT="$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo unknown)"
REPO_DIRTY="$(git -C "$REPO" status --porcelain 2>/dev/null | head -1 >/dev/null && echo true || echo false)"
MODULE_SHA="$(shasum -a 256 "$MODULE_FILE" 2>/dev/null | awk '{print $1}' || echo unknown)"
JAVA_VER="$(java -version 2>&1 | head -1 | sed 's/"/\\"/g' || echo unknown)"

# output counts
BUNDLES_TOTAL="$(find "$FHIR_DIR" -maxdepth 1 -name '*.json' \
  ! -name 'hospitalInformation*' ! -name 'practitionerInformation*' 2>/dev/null | wc -l | tr -d ' ')"
BUNDLES_PCA="$(grep -rlE '399068003|266569009' "$FHIR_DIR" 2>/dev/null | wc -l | tr -d ' ')"

export RUN_ID RUN_TS POP AGE GENDER STATE SEED CLINICIAN_SEED REFERENCE_DATE \
  SYNTHEA_VER SYNTHEA_COMMIT REPO_COMMIT REPO_DIRTY MODULE_FILE MODULE_SHA JAVA_VER \
  FHIR_DIR BUNDLES_TOTAL BUNDLES_PCA
python3 - "$(winpath "$PROV_DIR/$RUN_ID.json")" <<'PY'
import os, sys, json, platform
o = os.environ.get
doc = {
    "run_id": o("RUN_ID"),
    "timestamp_utc": o("RUN_TS"),
    "parameters": {
        "population": int(o("POP")), "age_range": o("AGE"), "gender": o("GENDER"),
        "state": o("STATE"), "seed": o("SEED"), "clinician_seed": o("CLINICIAN_SEED"),
        "reference_date": o("REFERENCE_DATE") or "today",
    },
    "generator": {
        "synthea_version": o("SYNTHEA_VER"), "synthea_commit": o("SYNTHEA_COMMIT"),
        "java": o("JAVA_VER"),
    },
    "module": {
        "file": os.path.relpath(o("MODULE_FILE"), o("MODULE_FILE").rsplit("/synthea-eu-cancer/",1)[0]+"/synthea-eu-cancer") if "/synthea-eu-cancer/" in o("MODULE_FILE") else o("MODULE_FILE"),
        "sha256": o("MODULE_SHA"), "repo_commit": o("REPO_COMMIT"),
        "repo_dirty": o("REPO_DIRTY") == "true",
    },
    "output": {
        "fhir_dir": o("FHIR_DIR"),
        "bundles_total": int(o("BUNDLES_TOTAL") or 0),
        "bundles_with_prostate_or_bph": int(o("BUNDLES_PCA") or 0),
        "note": "counts reflect all bundles currently in fhir_dir; clear it before a run for a per-run count",
    },
    "host": {"platform": platform.platform(), "user": os.environ.get("USER", "unknown")},
    "reproducibility": "Bit-identical given the same synthea_version + module.sha256 + seed + clinician_seed (+ reference_date for identical timelines).",
    "disclaimer": "Synthetic data. No real patient data; no resemblance to any real person. Not for medical use or medical research, and not for any diagnosis, treatment, or care decision. Provided only as interoperable example data for testing, development, validation, and education in European health-data sharing and analysis projects (e.g. EHDS, HL7 Europe Common Cancer Data Model). Provided 'as is', without warranty.",
}
with open(sys.argv[1], "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
# stable pointer to the newest run
with open(os.path.join(os.path.dirname(sys.argv[1]), "latest.json"), "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
print("Provenance:", sys.argv[1])
PY

# FHIR-native provenance: Provenance -> Group (+ Device/Organization/DocumentReference)
python3 "$(winpath "$REPO/scripts/make_provenance_fhir.py")" "$(winpath "$PROV_DIR/$RUN_ID.provenance.fhir.json")"
