# ECCDM draft profiles — vendored local build

`hl7.fhir.eu.cancer-common-c020f19.tgz` is an **unofficial, locally built** FHIR package of the
HL7 Europe Cancer Common (ECCDM) draft profiles. There is no published package yet (nothing on
packages.fhir.org or Simplifier as of 2026-08-27); the 13 draft profiles exist only as FSH sources.

**Source pin:** fork `ValhallasCat/cancer-common` @ `c020f196929a2d25e89d4f241b4465f7fd85cb73`
(2026-08-28, "change image, finalized after feedback, corrected typos") — 7 commits ahead of
`hl7-eu/cancer-common` master, containing the full profiling pass (all 11 logical models covered
by profiles).

**Build:** SUSHI 3.20.0, 0 errors → `fsh-generated/resources` + hand-written `package.json`
manifest (version `1.0.0-ballot.tnm-draft.c020f19`).

**Canonical:** `http://hl7.eu/fhir/cancer-common` — NOTE: the draft's own sushi-config carries a
"check if this may create issues" comment on this canonical, so it may change before ballot.
`scripts/postprocess_ccdm.py` therefore takes the base URL as a `--base` parameter.

**Use:**

```bash
# validate a generated bundle against the draft profiles
java -jar ~/.fhir/validator_cli.jar <bundle.json> -version 4.0.1 \
  -ig profiles/eccdm/hl7.fhir.eu.cancer-common-c020f19.tgz
# or run the gate over a sample:
scripts/validate_ccdm.sh
```

**Refresh:** re-run SUSHI on a newer fork/upstream commit, repack, replace the tgz, update the pin
here and in `provenance/`. When an official ballot package appears, delete this vendored copy and
depend on the registry package instead.
