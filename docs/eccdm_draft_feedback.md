# ECCDM draft profiles — implementer feedback from the synthea-eu-cancer pipeline

Reviewed/implemented against: fork `ValhallasCat/cancer-common` @ `c020f19` (2026-08-28),
built with SUSHI 3.20.0 (0 errors), used to profile a 1000-patient synthetic prostate cohort
(114 cancer journeys) and validated with the HL7 Java validator. Findings from actually
*implementing* the drafts, ordered by impact.

## Substantive

1. **Stage `component.code` guidance vs. example diverge.** The profile comment says TNM
   components are expected as codes `'T'`, `'N'`, `'M'`; the packaged example
   (`ObservationCancerStage1`) instead uses the **deprecated** PhenX LOINC codes
   67205-5/67206-3/67207-1 (all flagged "Deprecated" in LOINC) and LOINC LA answer codes as
   values. Recommendation: bind component codes explicitly (e.g. LOINC 21905-5 ff. or
   SNOMED 78873005/277206009/277208005) and allow SNOMED **UICC-8 qualifier values**
   (1352973007 `cT1c` etc.) as `component.value` — that is what registries carry, and AJCC
   codes are licence-encumbered while UICC values are plain SNOMED.
2. **No pathological-stage example.** Only a clinical stage example instance exists; the
   `EvidenceReference` extension description says pathological stages must reference "one
   surgery", but there is no example showing it. (Our implementation: same component set,
   `CinicalorPathological` = SNOMED 261023001, evidence → the prostatectomy Procedure.)
3. **`ObservationCancerStage.code` semantics unclear.** "For TNM, this element should be
   populated with 'TNM'" — with which system? The example uses LOINC 67204-8 ("Deprecated
   TNM *clinical* staging"), which conflicts with using the same code for pathological
   stage. A small required VS would remove the guesswork.
4. **Prostate TNM edge case worth documenting:** there is no pT1 (UICC 8th); TURP-incidental
   carcinomas are *clinical* cT1a/cT1b although specimen-derived. A note in the stage
   profile would prevent implementers from emitting invalid pT1.
5. **`procedure-surgery-eu-ccm` requires `bodySite` 1..1** — fine, but the example encodes
   it with ICD-O-3 topography while the Condition example uses ICD-10. Pick one (or bind a
   VS); mixed axes will fragment downstream analytics.
6. **Histology example value `8140/3` uses system `http://terminology.hl7.org/CodeSystem/icd-o-3`** —
   consider also allowing SNOMED morphology; note the classic SNOMED morphology code
   35917007 |Adenocarcinoma| was inactivated 2022-01-31 (active successor: 1187332001).

## Typos / cosmetics (grep-able)

- `ObservationHitsologyBehaviour` → Histology (profile name, observation-histology-behaviour-eu-ccm.fsh)
- `CinicalorPathological` → ClinicalOrPathological (extension name + slice, stage profile)
- `systematic-treatemmt-intent`, `systematic-treatemmt-ongoing` → treatment (extension ids —
  these leak into instance extension URLs, so fixing them later is a breaking change!)
- `EOCRadiotherpay1-Example`, `EOCSystemartictreatment1-Example` (instance ids)
- Radiotherapy example `radiotherapy-body-site` value has a stray `#`: `"code": "#C34.3"`
- Stage example lacks `subject` (validator best-practice warning); profile makes focus 1..
  but subject stays 0..1 — consider requiring subject too
- `sushi-config.yaml` canonical carries `# check if this may create issues` — please decide
  the canonical before ballot; downstream pipelines must pin it (ours parameterizes it).

## Offer

The pipeline produces CCDM-shaped synthetic prostate journeys (clinical + pathological TNM,
histology, AS/RT/systemic EpisodesOfCare, progression, last follow-up) — happy to contribute
them as additional IG examples or test data (CC0, SYNDERAI-tagged).
