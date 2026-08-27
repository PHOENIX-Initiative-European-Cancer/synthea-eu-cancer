#!/usr/bin/env python3
"""Post-process Synthea FHIR: tag every resource as synthetic (SYNDERAI convention).

SYNDERAI requires a synthetic-data marker on every generated resource. This is an
INDEPENDENT re-implementation of that convention (no SYNDERAI/AGPL code is used or
ported): we only reference the public CodeSystem URI as an identifier. Each resource
gets, in meta:
  - tag:      https://synderai.net/fhir/CodeSystem/tags#synthetic   (SYNDERAI marker)
  - security: http://terminology.hl7.org/CodeSystem/v3-ActReason#HTEST + #TRAIN
    (SYNDERAI convention; the earlier "SYNTH" code does not exist in v3-ActReason
    and made every resource fail base validation - fixed 2026-08-27)
Idempotent + additive. Bundle.entry[].resource are tagged; the Bundle itself too.

Usage: python3 scripts/postprocess_synthetic_tag.py [fhir_dir]
Default fhir_dir: synthea/output/fhir
"""
import json, os, sys, glob

SYNDERAI_SYS = "https://synderai.net/fhir/CodeSystem/tags"
SYNDERAI_TAG = {"system": SYNDERAI_SYS, "code": "synthetic", "display": "Synthetic data"}
SEC_HTEST = {"system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
             "code": "HTEST", "display": "test health data"}
SEC_TRAIN = {"system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
             "code": "TRAIN", "display": "training"}


def ensure_coding(meta, key, coding):
    """Add `coding` to meta[key] (tag/security) unless an entry with the same
    system+code is already present. Returns True if it was added."""
    lst = meta.setdefault(key, [])
    if any(c.get("system") == coding["system"] and c.get("code") == coding["code"] for c in lst):
        return False
    lst.append(dict(coding))
    return True


def tag_resource(res):
    if not isinstance(res, dict) or "resourceType" not in res:
        return False
    meta = res.setdefault("meta", {})
    added = ensure_coding(meta, "tag", SYNDERAI_TAG)
    added = ensure_coding(meta, "security", SEC_HTEST) or added
    added = ensure_coding(meta, "security", SEC_TRAIN) or added
    return added


def main():
    fhir = sys.argv[1] if len(sys.argv) > 1 else "synthea/output/fhir"
    files = glob.glob(os.path.join(fhir, "*.json"))
    n_files, n_changed, n_res = 0, 0, 0
    for fp in files:
        try:
            bundle = json.load(open(fp))
        except Exception:
            continue
        n_files += 1
        changed = tag_resource(bundle)  # tag the Bundle too
        for entry in bundle.get("entry", []):
            if tag_resource(entry.get("resource", {})):
                changed = True
                n_res += 1
        if changed:
            json.dump(bundle, open(fp, "w"), ensure_ascii=False)
            n_changed += 1
    print(f"scanned {n_files} bundles | modified {n_changed} | resources tagged {n_res}")


if __name__ == "__main__":
    main()
