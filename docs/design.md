# Design notes — synthea-eu-cancer

## Identifier-system convention (resolved — verified against SYNDERAI Patient templates)

SYNDERAI uses **two different conventions** depending on resource:

### Patient.identifier — up to 3 slices

| Slice | When | type | system | value |
|-------|------|------|--------|-------|
| 1 | always | `v2-0203#JHN` | `http://ec.europa.eu/identifier/eci` | ECI |
| 2 | optional | `v2-0203#MR` | `http://local.setting.eu/identifier` | external match ID |
| 3 | optional | `v2-0203#MR` | `http://local.setting.eu/identifier` | local ID (KVNR/BSN/Codice Fiscale-shaped) |

### Other resources (Bundle, Composition, Provider, ServiceRequest, …)

```
identifier.system = urn:oid:2.16.840.1.113883.2.51.999    (HL7 Europe examples branch)
```

### Key design insight

**No per-country FHIR identifier-system URIs are used anywhere.** Country realism lives in three places:

1. `address.country` (full name)
2. `nationality` extension → `valueCodeableConcept = urn:iso:std:iso:3166#<CC>` (EPS makes mandatory; EU Core conditional)
3. **Identifier value format** — KVNR-shape for DE persona, BSN-shape for NL, Codice Fiscale for IT — but always with `system = http://local.setting.eu/identifier`

This is deliberate: prevents synthetic IDs from colliding with real national identifier namespaces if a test bundle leaks into production, and avoids per-country IG drift.

→ synthea-eu-cancer must follow the same convention. `countries.yaml` should carry **identifier-value format hints** (length, pattern, check-digit algorithm) for generating realistic `localid` values — **not** FHIR system URIs.

### SYNDERAI synthetic-data tagging (mandatory on every resource)

```
meta.security = HTEST + TRAIN     (v3-ActReason)
meta.tag      = https://synderai.net/fhir/CodeSystem/tags#synthetic
```

Provided by the `syntheticDataPolicyMeta()` helper in SYNDERAI; we should mirror this.

## Open questions

- **Synthea integration**: submodule (`git submodule add https://github.com/synthetichealth/synthea synthea`) vs. fork? Submodule preferred — lets us track upstream releases and contribute fixes back, while keeping all EU-specific code in this repo.
- **CCDM target version**: HL7-EU Cancer Common Model v0.1.0 has `CancerTreatment.SystemicTreatment` at patient-data level. Track v0.2 / v0.3 as it matures (see beads-5vv).
- **Epidemiology source**: ECIS (European Cancer Information System) provides country-level incidence; ENCR (European Network of Cancer Registries) is the registry network. Need to decide: country-aggregate, NUTS-2, or registry-level granularity.
- **Pediatric oncology**: Synthea has no pediatric oncology modules out of the box. ICCC-3 (International Classification of Childhood Cancer) classification expected. Likely needs ground-up module authoring with input from pediatric oncology clinicians.
- **Phoenix Initiative cooperation**: how does this repo's output feed into Phoenix's CCDM IG testing? Best case = synthetic bundles become the reference test corpus for the IG's CI validation.
- **SYNDERAI cooperation**: scope of the partnership? (data generation pipeline, validation, distribution via the HL7-EU SYNDERAI showcase, …). SYNDERAI emphasizes purpose: *testing/validation, education, vendor implementation support* — not research analytics — so cohort design should optimize for breadth/coverage of profile variants over statistical fidelity.
- **Webinar deliverable** (2026-07-16): what's the demo? Likely a small CCDM-conformant cohort + the generator pipeline. Define the slide-ready artifact.

## Non-goals (initial)

- Not a fork of Synthea — stay on upstream
- Not a replacement for real cancer registry data
- Not a clinical decision support tool

## Workflow sketch

```
┌─────────────┐    ┌──────────────────┐    ┌────────────────┐
│  Synthea    │ ─► │  Synthea-FHIR    │ ─► │ HL7-EU CCDM    │
│  (upstream) │    │  bundles (R4)    │    │ conformant     │
│  + EU       │    │  per patient     │    │ bundles        │
│  modules    │    │                  │    │                │
└─────────────┘    └──────────────────┘    └────────────────┘
       ▲                                            │
       │                                            ▼
   EU epi data                              CCDM IG validator
   (ECIS/ENCR)                              (sushi + java validator)
```

## Mapping layer choices

Options for the Synthea-FHIR → CCDM transform:

1. **FHIR Mapping Language (FML)** — purest, executable, but tooling immature
2. **Python script using fhir.resources** — pragmatic, easy to debug
3. **HAPI Java transform** — heavy, but integrates with downstream HAPI test servers

Recommendation: start with Python (option 2) for prototyping; revisit FML once stable.
