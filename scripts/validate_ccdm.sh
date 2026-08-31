#!/usr/bin/env bash
# Validation gate: run the HL7 Java validator over a sample of generated cancer bundles
# against the vendored ECCDM draft package (profiles/eccdm/, see README there).
#
# Usage: scripts/validate_ccdm.sh [sample_size] [fhir_dir]
# Defaults: 3 cancer bundles from synthea/output/fhir.
#
# Exit code 0 = no ERRORs in the sampled bundles (warnings/notes tolerated - the
# draft profiles are FMM 0 and their terminology bindings are still in flux).
set -euo pipefail

SAMPLE="${1:-3}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
FHIR_DIR="${2:-$REPO/synthea/output/fhir}"
PKG="$REPO/profiles/eccdm/hl7.fhir.eu.cancer-common-c020f19.tgz"
VALIDATOR="${VALIDATOR_JAR:-$HOME/.fhir/validator_cli.jar}"
OUT_DIR="$REPO/synthea/output/validation_ccdm"
mkdir -p "$OUT_DIR"

# pick the first N bundles that carry the ECCDM cancer-condition profile
# (portable: no mapfile - macOS ships bash 3.2)
BUNDLES=()
while IFS= read -r line; do BUNDLES+=("$line"); done < <(
  grep -l 'cancer-condition-at-diagnosis-eu-ccm' "$FHIR_DIR"/*.json 2>/dev/null | head -n "$SAMPLE"
)
if [ "${#BUNDLES[@]}" -eq 0 ]; then
  echo "No ECCDM-tagged cancer bundles found in $FHIR_DIR - run postprocess_ccdm.py first." >&2
  exit 1
fi

echo "Validating ${#BUNDLES[@]} cancer bundle(s) against $(basename "$PKG")"
FAIL=0
for b in "${BUNDLES[@]}"; do
  name="$(basename "$b" .json)"
  log="$OUT_DIR/$name.validator.txt"
  echo "--- $name"
  if ! java -jar "$VALIDATOR" "$b" -version 4.0.1 -ig "$PKG" -tx n/a > "$log" 2>&1; then
    true # validator exits non-zero on errors; we grade from the log below
  fi
  tail -n 5 "$log" | sed 's/^/    /'
  if grep -qE '^\s*Error @' "$log"; then
    errs=$(grep -cE '^\s*Error @' "$log")
    echo "    -> $errs error(s), full log: ${log#$REPO/}"
    FAIL=1
  fi
done
exit $FAIL
