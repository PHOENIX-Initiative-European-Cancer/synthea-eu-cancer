#!/usr/bin/env python3
"""Emit a FHIR R4 provenance Bundle for one Synthea cohort generation run.

Standards-native counterpart to the JSON provenance doc: records WHAT was made
(a Group representing the cohort), by WHOM (Device = Synthea + seed, Organization
= Phoenix), and from WHICH SOURCE (DocumentReference = the calibrated module, by
SHA-256). Chosen shape: Provenance.target -> Group; entity -> DocumentReference.

Reads run facts from the environment (set by scripts/run_cohort.sh) and writes a
collection Bundle to argv[1] (+ a latest.provenance.fhir.json pointer).
"""
import os, sys, json, hashlib, base64

o = os.environ.get


def sha256_hex_to_b64(hexstr):
    try:
        return base64.b64encode(bytes.fromhex(hexstr)).decode()
    except Exception:
        return None


run_id = o("RUN_ID", "run_unknown")
ts = o("RUN_TS", "")
# ISO-8601 instant from the compact RUN_TS (YYYYMMDDTHHMMSSZ)
inst = ts
if len(ts) == 16 and ts.endswith("Z"):
    inst = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]}T{ts[9:11]}:{ts[11:13]}:{ts[13:15]}Z"

seed = o("SEED", "unknown")
cseed = o("CLINICIAN_SEED", "unknown")
ref_date = o("REFERENCE_DATE", "") or "today"
pop = o("POP", "0")
age = o("AGE", "")
gender = o("GENDER", "M")
state = o("STATE", "")
synthea_ver = o("SYNTHEA_VER", "unknown")
synthea_commit = o("SYNTHEA_COMMIT", "unknown")
repo_commit = o("REPO_COMMIT", "unknown")
module_sha = o("MODULE_SHA", "unknown")
bundles_total = int(o("BUNDLES_TOTAL", "0") or 0)
bundles_pca = int(o("BUNDLES_PCA", "0") or 0)

DISCLAIMER = (
    "Synthetic data. No real patient data; no resemblance to any real person. "
    "Not for medical use or medical research, and not for any diagnosis, treatment, "
    "or care decision. Provided only as interoperable example data for testing, "
    "development, validation, and education in European health-data sharing and "
    "analysis projects (e.g. EHDS, HL7 Europe Common Cancer Data Model). "
    "Provided 'as is', without warranty."
)

module_path = "modules/adult/prostate.json"
module_url = (
    f"https://raw.githubusercontent.com/PHOENIX-Initiative-European-Cancer/"
    f"synthea-eu-cancer/{repo_commit if repo_commit != 'unknown' else 'main'}/{module_path}"
)

dev_id = f"device-synthea-{run_id}"
org_id = "org-phoenix"
doc_id = f"module-prostate-{run_id}"
grp_id = f"cohort-{run_id}"
prov_id = f"provenance-{run_id}"

EXT = "https://phoenix-initiative.eu/fhir/StructureDefinition"

device = {
    "resourceType": "Device",
    "id": dev_id,
    "deviceName": [{"name": "Synthea Patient Generator", "type": "manufacturer-name"}],
    "version": [{"value": synthea_ver}],
    "property": [
        {"type": {"text": "seed"}, "valueCode": [{"text": str(seed)}]},
        {"type": {"text": "clinicianSeed"}, "valueCode": [{"text": str(cseed)}]},
        {"type": {"text": "syntheaCommit"}, "valueCode": [{"text": synthea_commit}]},
    ],
    "note": [{"text": f"Deterministic given identical version + module SHA-256 + seed {seed}"
                       f" + clinicianSeed {cseed} (+ referenceDate for identical timelines)."}],
}

org = {
    "resourceType": "Organization",
    "id": org_id,
    "name": "Phoenix Initiative (HL7 Europe)",
}

hash_b64 = sha256_hex_to_b64(module_sha)
doc = {
    "resourceType": "DocumentReference",
    "id": doc_id,
    "status": "current",
    "type": {"text": "Synthea generic module — prostate cancer pathway (calibrated)"},
    "description": f"SHA-256: {module_sha}",
    "content": [{
        "attachment": {
            "contentType": "application/json",
            "url": module_url,
            "title": module_path,
            **({"hash": hash_b64} if hash_b64 else {}),
        }
    }],
    "identifier": [{"system": "urn:sha-256", "value": module_sha}],
}

SYNTH_SECURITY = [{
    "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
    "code": "SYNTH", "display": "synthetic data",
}]

group = {
    "resourceType": "Group",
    "id": grp_id,
    "meta": {"security": SYNTH_SECURITY},
    "text": {"status": "generated",
             "div": f'<div xmlns="http://www.w3.org/1999/xhtml"><p><b>Synthetic cohort.</b> {DISCLAIMER}</p></div>'},
    "type": "person",
    "actual": True,
    "quantity": bundles_total,
    "code": {"text": "Synthetic prostate-pathway cohort (Synthea)"},
    "characteristic": [
        {"code": {"text": "gender"},
         "valueCodeableConcept": {"text": "male" if gender.upper().startswith("M") else gender},
         "exclude": False},
        {"code": {"text": "age at generation (years)"},
         "valueRange": {"low": {"value": int(age.split("-")[0])}, "high": {"value": int(age.split("-")[1])}}
         if "-" in age else {"text": age}, "exclude": False},
        {"code": {"text": "demographic basis"},
         "valueCodeableConcept": {"text": state}, "exclude": False},
    ],
    "extension": [
        {"url": f"{EXT}/cohort-bundles-total", "valueInteger": bundles_total},
        {"url": f"{EXT}/cohort-bundles-with-prostate-or-bph", "valueInteger": bundles_pca},
    ],
}

provenance = {
    "resourceType": "Provenance",
    "id": prov_id,
    "target": [{"reference": f"Group/{grp_id}"}],
    "occurredDateTime": inst,
    "recorded": inst,
    "activity": {"coding": [{
        "system": "http://terminology.hl7.org/CodeSystem/v3-DataOperation",
        "code": "CREATE", "display": "create"}]},
    "agent": [
        {"type": {"coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
            "code": "assembler"}]},
         "who": {"reference": f"Device/{dev_id}"}},
        {"type": {"coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
            "code": "custodian"}]},
         "who": {"reference": f"Organization/{org_id}"}},
    ],
    "entity": [{"role": "source", "what": {"reference": f"DocumentReference/{doc_id}"}}],
    "extension": [
        {"url": f"{EXT}/generation-seed", "valueString": str(seed)},
        {"url": f"{EXT}/generation-clinician-seed", "valueString": str(cseed)},
        {"url": f"{EXT}/generation-reference-date", "valueString": str(ref_date)},
        {"url": f"{EXT}/generation-population-requested", "valueInteger": int(pop)},
        {"url": f"{EXT}/synthetic-data-disclaimer", "valueString": DISCLAIMER},
    ],
}
provenance["meta"] = {"security": SYNTH_SECURITY}

bundle = {
    "resourceType": "Bundle",
    "id": f"provenance-bundle-{run_id}",
    "type": "collection",
    "timestamp": inst,
    "entry": [
        {"fullUrl": f"Provenance/{prov_id}", "resource": provenance},
        {"fullUrl": f"Group/{grp_id}", "resource": group},
        {"fullUrl": f"Device/{dev_id}", "resource": device},
        {"fullUrl": f"Organization/{org_id}", "resource": org},
        {"fullUrl": f"DocumentReference/{doc_id}", "resource": doc},
    ],
}

out = sys.argv[1]
with open(out, "w") as f:
    json.dump(bundle, f, indent=2, ensure_ascii=False)
with open(os.path.join(os.path.dirname(out), "latest.provenance.fhir.json"), "w") as f:
    json.dump(bundle, f, indent=2, ensure_ascii=False)
print("FHIR provenance:", out)
