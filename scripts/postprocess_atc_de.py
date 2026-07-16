#!/usr/bin/env python3
"""Post-process Synthea FHIR: restore the dual ATC coding (WHO + BfArM/ATC-DE).

Synthea's FHIR exporter keeps only the FIRST coding per medication, so the
BfArM/ATC-DE coding authored in the module (per MII-Onko #283) is dropped from
the generated bundles. This step re-adds it: for every medication coding that
uses the WHO ATC system, it appends a sibling coding with the German BfArM/ATC-DE
system and the same code (ATC-DE shares the WHO code). Idempotent + additive.

Usage: python3 scripts/postprocess_atc_de.py [fhir_dir]
Default fhir_dir: synthea/output/fhir
"""
import json, os, sys, glob

WHO = "http://www.whocc.no/atc"
DE = "http://fhir.de/CodeSystem/bfarm/atc"


def fix_codeable(cc):
    """Return True if a DE coding was added to this CodeableConcept."""
    if not isinstance(cc, dict):
        return False
    codings = cc.get("coding")
    if not isinstance(codings, list):
        return False
    changed = False
    for c in list(codings):
        if c.get("system") == WHO and c.get("code"):
            code = c["code"]
            already = any(d.get("system") == DE and d.get("code") == code for d in codings)
            if not already:
                de = {"system": DE, "code": code}
                if c.get("display"):
                    de["display"] = c["display"]
                # place the DE coding directly after its WHO sibling
                codings.insert(codings.index(c) + 1, de)
                changed = True
    return changed


def walk(obj):
    """Recursively find every medicationCodeableConcept / code CC carrying ATC."""
    changed = False
    if isinstance(obj, dict):
        for key in ("medicationCodeableConcept", "code"):
            if key in obj and fix_codeable(obj[key]):
                changed = True
        for v in obj.values():
            if isinstance(v, (dict, list)) and walk(v):
                changed = True
    elif isinstance(obj, list):
        for v in obj:
            if walk(v):
                changed = True
    return changed


def main():
    fhir = sys.argv[1] if len(sys.argv) > 1 else "synthea/output/fhir"
    files = glob.glob(os.path.join(fhir, "*.json"))
    n_files, n_changed, n_codings = 0, 0, 0
    for fp in files:
        try:
            bundle = json.load(open(fp))
        except Exception:
            continue
        n_files += 1
        before = json.dumps(bundle).count(DE)
        if walk(bundle):
            after = json.dumps(bundle).count(DE)
            n_codings += (after - before)
            json.dump(bundle, open(fp, "w"), ensure_ascii=False)
            n_changed += 1
    print(f"scanned {n_files} bundles | modified {n_changed} | DE codings added {n_codings}")


if __name__ == "__main__":
    main()
