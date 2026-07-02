#!/usr/bin/env python3
"""FHIR bundles -> process-mining event log (CSV) for the prostate pathway.

Each Synthea patient becomes a CASE; each timestamped prostate-relevant resource
becomes an EVENT (activity + timestamp). Output is a tidy event log that imports
directly into Disco / ProM / Celonis / PM4Py, plus a quick trace-variant analysis.

Usage:
  python3 scripts/fhir_to_eventlog.py [fhir_dir] [out_csv]
Defaults: synthea/output/fhir  ->  output/prostate_eventlog.csv
"""
import json, os, sys, glob, csv
from collections import Counter, defaultdict

# --- prostate-pathway activity map (validated codes; see terminology/snomed_data_dictionary.md) ---
ACT = {
    # Encounter
    "185345009": "Presentation: LUTS (urology)",
    # Conditions
    "266569009": "Diagnosis: BPH",
    "399068003": "Diagnosis: Prostate cancer",
    # Procedures
    "410006001": "DRE",
    "429820004": "TRUS (endorectal US)",
    "1144760005": "mpMRI",
    "236258004": "Prostate biopsy",
    "26294005": "Radical prostatectomy",
    "90199006": "TURP",
    "33195004": "Radiotherapy (EBRT)",
    # Observations (LOINC)
    "2857-1": "PSA test",
    "82717-8": "PI-RADS",
    "35266-6": "Gleason score",
    # Care plans
    "424313000": "Active surveillance",
    "373818007": "Watchful waiting",
    # Medications (ATC, WHO + DE share the code)
    "G04CA02": "Med: tamsulosin",
    "G04CB01": "Med: finasteride",
    "L02AE02": "Med: leuprorelin (ADT)",
    "L02BB04": "Med: enzalutamide (ARPI)",
    "L01CD02": "Med: docetaxel",
    "L01CD04": "Med: cabazitaxel",
}
TS_FIELDS = ["performedDateTime", "effectiveDateTime", "authoredOn", "onsetDateTime", "recordedDate"]

def codes_of(res):
    out = []
    for key in ("code", "medicationCodeableConcept"):
        cc = res.get(key)
        if isinstance(cc, dict):
            for c in cc.get("coding", []):
                if c.get("code"):
                    out.append(str(c["code"]))
    return out

def timestamp_of(res):
    for f in TS_FIELDS:
        if res.get(f):
            return res[f]
    for f in ("performedPeriod", "period", "effectivePeriod"):
        p = res.get(f)
        if isinstance(p, dict) and p.get("start"):
            return p["start"]
    return None

def main():
    fhir = sys.argv[1] if len(sys.argv) > 1 else "synthea/output/fhir"
    out = sys.argv[2] if len(sys.argv) > 2 else "output/prostate_eventlog.csv"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    rows = []
    files = [f for f in glob.glob(os.path.join(fhir, "*.json"))
             if not os.path.basename(f).lower().startswith(("hospitalinformation", "practitionerinformation"))]
    for fp in files:
        try:
            bundle = json.load(open(fp))
        except Exception:
            continue
        case = None
        for e in bundle.get("entry", []):
            if e.get("resource", {}).get("resourceType") == "Patient":
                case = e["resource"].get("id") or os.path.basename(fp)
                break
        if not case:
            continue
        for e in bundle.get("entry", []):
            res = e.get("resource", {})
            for code in codes_of(res):
                if code in ACT:
                    ts = timestamp_of(res)
                    if ts:
                        rows.append((case, ACT[code], ts, res.get("resourceType", "")))
                    break
        # death as a terminal event (competing-risk vs prostate-cancer specific)
        dts, cod = None, set()
        for e in bundle.get("entry", []):
            r = e.get("resource", {})
            if r.get("resourceType") == "Patient" and r.get("deceasedDateTime"):
                dts = r["deceasedDateTime"]
            if r.get("resourceType") == "Observation" and \
               any(c.get("code") == "69453-9" for c in r.get("code", {}).get("coding", [])):
                for c in r.get("valueCodeableConcept", {}).get("coding", []):
                    if c.get("code"):
                        cod.add(str(c["code"]))
        if dts:
            act = "Death (prostate cancer)" if "399068003" in cod else "Death (other cause)"
            rows.append((case, act, dts, "Patient"))
    rows.sort(key=lambda r: (r[0], r[2]))
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case_id", "activity", "timestamp", "resource_type"])
        w.writerows(rows)

    # --- quick trace-variant analysis (mini process mining) ---
    traces = defaultdict(list)
    for case, act, ts, _ in rows:
        traces[case].append(act)
    variants = Counter(tuple(v) for v in traces.values())
    print(f"Event log written: {out}")
    print(f"Cases: {len(traces)} | Events: {len(rows)} | Distinct activities: {len(set(r[1] for r in rows))}")
    print(f"Distinct trace variants: {len(variants)}")
    print("\nTop 8 variants:")
    for var, n in variants.most_common(8):
        print(f"  {n:3}x  {' -> '.join(var)}")

if __name__ == "__main__":
    main()
