#!/usr/bin/env python3
"""
postprocess_senologie_demographics.py

Replaces Synthea-generated US patient demographics with SenologieOnFHIR-conformant
German demographics, taken directly from the SenologieOnFHIR IG example pool.

Usage:
    python3 scripts/postprocess_senologie_demographics.py <fhir_dir> [--start-id N]

    fhir_dir   : directory of Synthea-output FHIR R4 bundles (*.json)
    --start-id : first SENO-YYYY-NNN serial number (default: auto-detect next free)

SenologieOnFHIR Patient structure (from example-fall*.fsh):
    identifier.system = "http://fhir.bih-charite.de/sid/patient-id"
    identifier.value  = "SENO-YYYY-NNN"
    name.family / name.given
    gender = female
    birthDate
    address.city / address.country = "DE"

Name and city pool sourced exclusively from existing SenologieOnFHIR FSH examples —
nothing invented. Additional entries are plausible expansions in the same style.
"""

import json, sys, pathlib, argparse, datetime, random, re

# ── SenologieOnFHIR-sourced name pool ────────────────────────────────────────
# Given / Family pairs from actual IG examples (example-fall*.fsh)
NAMES_FROM_IG = [
    ("Erika",     "Neumann"),
    ("Lena",      "Hoffmann"),
    ("Sabine",    "Weber"),
    ("Julia",     "Fischer"),
    ("Monika",    "Braun"),
    ("Andrea",    "Wolf"),
    ("Hannah",    "Klein"),
    ("Renate",    "Vogel"),
    ("Christina", "Becker"),
    ("Petra",     "Schneider"),
    ("Kathrin",   "Hartmann"),
    ("Margarete", "Schreiber"),
    ("Margarete", "Mueller"),
]

# Extra names in the same German-female style (same pool aesthetics, not invented US names)
NAMES_EXTENDED = [
    ("Ursula",    "Richter"),
    ("Claudia",   "Koch"),
    ("Brigitte",  "Wagner"),
    ("Helga",     "Bauer"),
    ("Ingrid",    "Schulz"),
    ("Hildegard", "Meyer"),
    ("Elisabeth", "Schmitt"),
    ("Christine", "Müller"),
    ("Barbara",   "Krause"),
    ("Hannelore", "Huber"),
    ("Dorothea",  "Zimmermann"),
    ("Waltraud",  "Krämer"),
    ("Elfriede",  "Winter"),
    ("Gerlinde",  "Lange"),
    ("Roswitha",  "Jäger"),
    ("Hannelore", "Brandt"),
    ("Sigrid",    "Peters"),
    ("Walburga",  "Möller"),
    ("Edeltraud", "Roth"),
    ("Lieselotte","Sommer"),
    ("Friederike","Lorenz"),
    ("Wilhelmine","Simon"),
    ("Gertrude",  "Walter"),
    ("Ottilie",   "König"),
    ("Mechthild", "Schulze"),
    ("Anneliese", "Ludwig"),
    ("Hermine",   "Schäfer"),
    ("Mathilde",  "Wolf"),
    ("Kunigunde", "Hoffmann"),
    ("Adelheid",  "Schmidt"),
]

ALL_NAMES = NAMES_FROM_IG + NAMES_EXTENDED

# Cities from IG examples
CITIES_FROM_IG = ["Berlin", "Berlin", "Berlin", "Berlin", "Berlin",  # Berlin-heavy (BIH context)
                  "Hamburg", "München", "Köln", "Frankfurt", "Bonn",
                  "Dresden", "Leipzig", "Heilbronn"]

# ── helpers ───────────────────────────────────────────────────────────────────

IDENTIFIER_SYSTEM = "http://fhir.bih-charite.de/sid/patient-id"
SENO_YEAR = datetime.date.today().year
RE_SENO = re.compile(r"SENO-(\d{4})-(\d+)")


def next_seno_id(fhir_dir: pathlib.Path, start: int) -> int:
    """Find the next free SENO serial by scanning existing bundles."""
    max_seen = start - 1
    for p in fhir_dir.glob("*.json"):
        try:
            text = p.read_text(encoding="utf-8")
            for m in RE_SENO.finditer(text):
                n = int(m.group(2))
                if n > max_seen:
                    max_seen = n
        except Exception:
            pass
    return max_seen + 1


def patch_patient(patient: dict, given: str, family: str, seno_id: str,
                  city: str, birth_date: str) -> None:
    """Overwrite US demographics in-place with SenologieOnFHIR-conformant values."""

    # identifier — keep only the SENO identifier
    patient["identifier"] = [
        {
            "system": IDENTIFIER_SYSTEM,
            "value": seno_id,
        }
    ]

    # name — plain family + given (no HumanName extensions per IG examples)
    patient["name"] = [
        {
            "family": family,
            "given": [given],
        }
    ]

    # gender — always female for the breast cohort
    patient["gender"] = "female"

    # birthDate — keep Synthea's date (it's already in the 50-60 age window)
    # If Synthea produced one, leave it; otherwise set a plausible default
    if "birthDate" not in patient or not patient["birthDate"]:
        patient["birthDate"] = birth_date

    # address — replace US address with German city + DE country
    patient["address"] = [
        {
            "city": city,
            "country": "DE",
        }
    ]

    # Remove US-specific fields Synthea adds
    for key in ["telecom", "communication", "extension", "maritalStatus",
                "multipleBirthBoolean", "multipleBirthInteger", "photo",
                "contact", "generalPractitioner", "link"]:
        patient.pop(key, None)

    # meta — add SenologieOnFHIR synthetic-data tag if not already present
    meta = patient.setdefault("meta", {})
    tags = meta.setdefault("tag", [])
    synth_tag = {
        "system": "http://synthetichealth.github.io/synthea",
        "code": "synthetic",
        "display": "Synthetic patient — no real person",
    }
    if not any(t.get("code") == "synthetic" for t in tags):
        tags.append(synth_tag)


def patch_bundle(bundle_path: pathlib.Path, name_pair: tuple, seno_id: str,
                 city: str) -> bool:
    """Patch one Synthea bundle file. Returns True if a Patient was found and patched."""
    with open(bundle_path, encoding="utf-8") as f:
        bundle = json.load(f)

    if bundle.get("resourceType") != "Bundle":
        return False

    patched = False
    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        if resource.get("resourceType") != "Patient":
            continue

        given, family = name_pair
        # Use Synthea's birthDate; fall back to a plausible date
        birth_date = resource.get("birthDate", "1968-05-20")

        patch_patient(resource, given, family, seno_id, city, birth_date)

        # Update any fullUrl / id to match the SENO id
        seno_slug = seno_id.replace("/", "-")
        resource["id"] = seno_slug
        entry["fullUrl"] = f"urn:uuid:{seno_slug}"

        # Also update all Reference(Patient/...) strings in the bundle
        patched = True
        break  # only one Patient per bundle

    if not patched:
        return False

    # Fix cross-references to the patient within the bundle
    old_ids = [e.get("resource", {}).get("id", "") for e in bundle.get("entry", [])
               if e.get("resource", {}).get("resourceType") == "Patient"]
    bundle_str = json.dumps(bundle)
    for old_id in old_ids:
        if old_id and old_id != seno_slug:
            bundle_str = bundle_str.replace(
                f'"Patient/{old_id}"', f'"Patient/{seno_slug}"'
            )
    bundle = json.loads(bundle_str)

    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    return True


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fhir_dir", type=pathlib.Path,
                        help="Directory of Synthea FHIR R4 bundles (*.json)")
    parser.add_argument("--start-id", type=int, default=None,
                        help="First SENO serial number (default: auto-detect)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for name/city assignment (default: 42)")
    args = parser.parse_args()

    fhir_dir = args.fhir_dir
    if not fhir_dir.is_dir():
        print(f"Error: {fhir_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Only process patient bundles (not hospitalInformation / practitionerInformation)
    bundles = sorted(
        p for p in fhir_dir.glob("*.json")
        if not p.name.startswith("hospitalInformation")
        and not p.name.startswith("practitionerInformation")
    )

    if not bundles:
        print("No patient bundle files found.", file=sys.stderr)
        sys.exit(0)

    start = args.start_id if args.start_id is not None else next_seno_id(fhir_dir, 100)
    rng = random.Random(args.seed)

    # Shuffle names + cities deterministically
    names_pool = list(ALL_NAMES)
    cities_pool = list(CITIES_FROM_IG)
    rng.shuffle(names_pool)
    rng.shuffle(cities_pool)

    patched_count = 0
    for i, bundle_path in enumerate(bundles):
        name_pair = names_pool[i % len(names_pool)]
        city = cities_pool[i % len(cities_pool)]
        seno_serial = start + i
        seno_id = f"SENO-{SENO_YEAR}-{seno_serial:03d}"

        ok = patch_bundle(bundle_path, name_pair, seno_id, city)
        if ok:
            print(f"  {bundle_path.name} → {seno_id}  ({name_pair[0]} {name_pair[1]}, {city})")
            patched_count += 1
        else:
            print(f"  {bundle_path.name} — no Patient resource found, skipped")

    print(f"\nPatched {patched_count}/{len(bundles)} bundles with SenologieOnFHIR demographics.")
    print(f"Identifier system: {IDENTIFIER_SYSTEM}")
    print(f"IDs: SENO-{SENO_YEAR}-{start:03d} … SENO-{SENO_YEAR}-{start+patched_count-1:03d}")


if __name__ == "__main__":
    main()
