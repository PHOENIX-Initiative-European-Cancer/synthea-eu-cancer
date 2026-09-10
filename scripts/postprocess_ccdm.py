#!/usr/bin/env python3
"""ECCDM layer: reshape Synthea prostate bundles to HL7-EU Cancer Common (CCDM) draft profiles.

Runs AFTER postprocess_atc_de.py / postprocess_synthetic_tag.py. Only bundles containing a
prostate-cancer Condition (SNOMED 399068003) are touched; all other bundles pass through unchanged.

Per cancer bundle:
  in-place upgrades
    Patient                -> meta.profile patient-eu-ccm
    Condition 399068003    -> cancer-condition-at-diagnosis-eu-ccm (+ bodySite prostate,
                              + diagnosis-date extension: BiopsyDate from needle biopsy, else VisitDate)
    Observation 59847-4    -> observation-histology-behaviour-eu-ccm (+ code 395531003,
                              + ICD-O-3 8140/3 value coding, + focus condition)
    Procedure 26294005 RP  -> procedure-surgery-eu-ccm (+ surgery-intent curative, + reasonReference)
  derived resources (deterministic uuid5 ids, appended to the bundle)
    ObservationCancerStage       clinical (from 21905-5/21906-3/21907-1) + pathological (21899-0/21900-6)
    EpisodeOfCare surveillance   from Active-surveillance CarePlan 424313000
    EpisodeOfCare radiotherapy   from EBRT procedures 33195004
    EpisodeOfCare systemic tx    from ADT/ARPI/taxane MedicationRequests (ATC)
    ClinicalCancerProgression    from recurrent-PCa Condition 1098981000119101
    LastFollowUp                 from last encounter / deceasedDateTime

Profile base URL is configurable (--base) because the draft's canonical may still change
(sushi-config.yaml carries a '# check if this may create issues' comment on it).
Draft pin: ValhallasCat/cancer-common @ c020f19 (2026-08-28), vendored in profiles/eccdm/.
(c020f19 split the stage EvidenceReference into cancer-stage-evidence-reference-imaging /
-surgery and added the optional cancer-histology-behaviour-reference on the Condition.)
Calibration & code provenance: epidemiology/prostate_calibration.md §11.
"""
import argparse
import glob
import json
import os
import sys
import uuid

SCT = 'http://snomed.info/sct'
LOINC = 'http://loinc.org'
ICDO3 = 'http://terminology.hl7.org/CodeSystem/icd-o-3'

PCA_CODE = '399068003'
RECURRENT_CODE = '1098981000119101'
BIOPSY_CODE = '236258004'
MPMRI_CODE = '1144760005'
RP_CODE = '26294005'
EBRT_CODES = {'33195004'}
AS_CAREPLAN_CODE = '424313000'
ADT_ATC = {'L02AE02', 'L02BB04'}      # leuprorelin, enzalutamide
TAXANE_ATC = {'L01CD02', 'L01CD04'}   # docetaxel, cabazitaxel

CT_OBS, CN_OBS, CM_OBS = '21905-5', '21906-3', '21907-1'
PT_OBS, PN_OBS = '21899-0', '21900-6'
HIST_OBS = '59847-4'

CLINICAL_STAGING = {'code': '260998006', 'system': SCT, 'display': 'Clinical staging (qualifier value)'}
PATHOLOGICAL_STAGING = {'code': '261023001', 'system': SCT, 'display': 'Pathological staging (qualifier value)'}
CURATIVE = {'code': '373808002', 'system': SCT, 'display': 'Curative - procedure intent (qualifier value)'}
PALLIATIVE = {'code': '363676003', 'system': SCT, 'display': 'Palliative - procedure intent (qualifier value)'}

# component codes as used by the IG's own ObservationCancerStage example (PhenX panel)
STAGE_CODE = {'code': '67204-8', 'system': LOINC, 'display': 'Deprecated TNM clinical staging [PhenX]'}
COMP_T = {'code': '67205-5', 'system': LOINC, 'display': 'Deprecated TNM clinical staging - primary tumor - T [PhenX]'}
COMP_N = {'code': '67206-3', 'system': LOINC, 'display': 'Deprecated TNM clinical staging - nodal involvement - N [PhenX]'}
COMP_M = {'code': '67207-1', 'system': LOINC, 'display': 'Deprecated TNM clinical staging - distant metastases - M [PhenX]'}

NS = uuid.uuid5(uuid.NAMESPACE_URL, 'https://synderai.net/synthea-eu-cancer/ccdm')

SYNTHETIC_TAG_META = None  # captured from bundle resources so derived resources match the convention


def cc(coding, text=None):
    out = {'coding': [coding]}
    if text:
        out['text'] = text
    return out


def first_coding(codeable, system_hint=None):
    for coding in (codeable or {}).get('coding', []):
        if system_hint is None or system_hint in coding.get('system', ''):
            return coding
    return None


def obs_code(resource):
    coding = first_coding(resource.get('code'))
    return coding.get('code') if coding else None


def add_profile(resource, url):
    meta = resource.setdefault('meta', {})
    profiles = meta.setdefault('profile', [])
    if url not in profiles:
        profiles.append(url)


def effective(resource):
    return (resource.get('effectiveDateTime')
            or (resource.get('effectivePeriod') or {}).get('start')
            or resource.get('performedDateTime')
            or (resource.get('performedPeriod') or {}).get('start')
            or resource.get('onsetDateTime')
            or resource.get('authoredOn'))


class BundleCtx:
    def __init__(self, bundle):
        self.bundle = bundle
        self.entries = bundle.get('entry', [])
        self.by_type = {}
        self.ref_of = {}
        for entry in self.entries:
            resource = entry.get('resource')
            if not resource:
                continue
            self.by_type.setdefault(resource['resourceType'], []).append(resource)
            self.ref_of[id(resource)] = entry.get('fullUrl') or f"{resource['resourceType']}/{resource.get('id')}"
        self.patient = (self.by_type.get('Patient') or [None])[0]
        self.request_style = next((e.get('request') for e in self.entries if e.get('request')), None)
        meta = (self.patient or {}).get('meta', {})
        self.tag = meta.get('tag')
        self.security = meta.get('security')

    def ref(self, resource):
        return {'reference': self.ref_of[id(resource)]}

    def append(self, resource, kind):
        rid = str(uuid.uuid5(NS, f"{self.patient.get('id')}|{kind}"))
        resource['id'] = rid
        meta = resource.setdefault('meta', {})
        if self.tag:
            meta['tag'] = self.tag
        if self.security:
            meta['security'] = self.security
        full_url = f'urn:uuid:{rid}'
        # upsert: deterministic ids make re-runs replace instead of duplicate
        for entry in self.entries:
            if entry.get('fullUrl') == full_url:
                entry['resource'] = resource
                self.ref_of[id(resource)] = full_url
                return resource
        entry = {'fullUrl': full_url, 'resource': resource}
        if self.request_style:
            entry['request'] = {'method': self.request_style.get('method', 'POST'),
                                'url': resource['resourceType']}
        self.entries.append(entry)
        self.ref_of[id(resource)] = full_url
        self.by_type.setdefault(resource['resourceType'], []).append(resource)
        return resource


def find_cancer_condition(ctx):
    conditions = [c for c in ctx.by_type.get('Condition', [])
                  if (first_coding(c.get('code'), SCT) or first_coding(c.get('code')) or {}).get('code') == PCA_CODE]
    conditions.sort(key=lambda c: c.get('onsetDateTime') or '')
    return conditions[0] if conditions else None


def procedures_with_code(ctx, codes):
    out = []
    for procedure in ctx.by_type.get('Procedure', []):
        coding = first_coding(procedure.get('code'))
        if coding and coding.get('code') in codes:
            out.append(procedure)
    out.sort(key=lambda p: effective(p) or '')
    return out


def process_bundle(path, base, stats):
    with open(path) as f:
        bundle = json.load(f)
    ctx = BundleCtx(bundle)
    if not ctx.patient:
        return False
    condition = find_cancer_condition(ctx)
    if condition is None:
        return False
    profile = lambda name: f'{base}/StructureDefinition/{name}'
    ext = lambda name: f'{base}/StructureDefinition/{name}'
    condition_ref = ctx.ref(condition)
    patient_ref = ctx.ref(ctx.patient)

    # --- Patient ---
    add_profile(ctx.patient, profile('patient-eu-ccm'))
    # drop Synthea-internal QALY/DALY extensions: their URLs do not resolve, which fails
    # base validation and cascades into every reference-target profile check
    if ctx.patient.get('extension'):
        ctx.patient['extension'] = [e for e in ctx.patient['extension']
                                    if 'synthetichealth.github.io' not in e.get('url', '')]
        if not ctx.patient['extension']:
            del ctx.patient['extension']

    # --- Condition at diagnosis ---
    add_profile(condition, profile('cancer-condition-at-diagnosis-eu-ccm'))
    condition.setdefault('bodySite', [cc({'system': SCT, 'code': '41216001',
                                          'display': 'Prostatic structure (body structure)'})])
    onset = condition.get('onsetDateTime')
    biopsies = [p for p in procedures_with_code(ctx, {BIOPSY_CODE})
                if onset is None or (effective(p) or '') <= onset]
    dd_ext = {'url': ext('diagnosis-date'), 'extension': []}
    if biopsies:
        dd_ext['extension'].append({'url': 'BiopsyDate', 'valueDateTime': effective(biopsies[-1])})
    elif onset:
        dd_ext['extension'].append({'url': 'VisitDate', 'valueDateTime': onset})
    if dd_ext['extension'] and not any(e.get('url') == ext('diagnosis-date')
                                       for e in condition.get('extension', [])):
        condition.setdefault('extension', []).append(dd_ext)

    # --- Histology/behaviour ---
    for histology in ctx.by_type.get('Observation', []):
        if obs_code(histology) != HIST_OBS:
            continue
        add_profile(histology, profile('observation-histology-behaviour-eu-ccm'))
        code = histology.setdefault('code', {'coding': []})
        if not first_coding(code, SCT):
            code['coding'].insert(0, {'system': SCT, 'code': '395531003',
                                      'display': 'Neoplasm observable (observable entity)'})
        value = histology.get('valueCodeableConcept')
        if value and not first_coding(value, 'icd-o'):
            value['coding'].append({'system': ICDO3, 'code': '8140/3', 'display': 'Adenocarcinoma, NOS'})
        histology.setdefault('focus', [condition_ref])
        # c020f19: optional back-reference Condition -> HistologyBehaviour observation
        cond_exts = condition.setdefault('extension', [])
        if not any(e.get('url') == ext('cancer-histology-behaviour-reference') for e in cond_exts):
            cond_exts.append({'url': ext('cancer-histology-behaviour-reference'),
                              'valueReference': ctx.ref(histology)})

    # --- Surgery (RP incl. salvage RP) ---
    rp_procedures = procedures_with_code(ctx, {RP_CODE})
    for rp in rp_procedures:
        add_profile(rp, profile('procedure-surgery-eu-ccm'))
        exts = rp.setdefault('extension', [])
        if not any(e.get('url') == ext('surgery-intent') for e in exts):
            exts.append({'url': ext('surgery-intent'), 'valueCodeableConcept': cc(CURATIVE)})
        rp.setdefault('reasonReference', [condition_ref])
        # profile requires bodySite 1..1
        rp.setdefault('bodySite', [cc({'system': SCT, 'code': '41216001',
                                       'display': 'Prostatic structure (body structure)'})])
        # profile's closed slicing on performed[x] admits only performedDateTime
        if 'performedPeriod' in rp:
            rp['performedDateTime'] = rp['performedPeriod'].get('start')
            del rp['performedPeriod']

    # --- Cancer stage observations ---
    tnm = {k: [] for k in (CT_OBS, CN_OBS, CM_OBS, PT_OBS, PN_OBS)}
    for observation in ctx.by_type.get('Observation', []):
        code = obs_code(observation)
        if code in tnm:
            tnm[code].append(observation)
    m1 = any(first_coding(o.get('valueCodeableConcept'), SCT) and
             'M1' in (first_coding(o.get('valueCodeableConcept'), SCT).get('display') or '')
             for o in tnm[CM_OBS])

    def stage_obs(kind, members, comp_codes, staging_qualifier, evidence, evidence_ext):
        components = []
        for member, comp_code in zip(members, comp_codes):
            value_coding = first_coding(member.get('valueCodeableConcept'), SCT)
            if value_coding:
                components.append({'code': cc(comp_code), 'valueCodeableConcept': cc(value_coding)})
        if not components:
            return
        stage = {
            'resourceType': 'Observation',
            'meta': {'profile': [profile('observation-cancer-stage-eu-ccm')]},
            'status': 'final',
            'code': cc(STAGE_CODE, text='TNM'),
            'subject': patient_ref,
            'focus': [condition_ref],
            'component': components,
            'extension': [{'url': ext('clinical-or-pathological'),
                           'valueCodeableConcept': cc(staging_qualifier)}],
        }
        when = effective(members[0])
        if when:
            stage['effectiveDateTime'] = when
        if evidence is not None:
            stage['extension'].append({'url': ext(evidence_ext),
                                       'valueReference': ctx.ref(evidence)})
        ctx.append(stage, kind)
        stats[kind] += 1

    # clinical evidence must be an ObservationImaging (the profile's EvidenceReference only
    # admits ObservationImaging | ProcedureSurgery) -> derive one from the mpMRI procedure
    mpmri = procedures_with_code(ctx, {MPMRI_CODE})
    imaging_obs = None
    if mpmri:
        imaging_obs = {
            'resourceType': 'Observation',
            'meta': {'profile': [profile('observation-imaging-eu-ccm')]},
            'status': 'final',
            'code': cc({'system': SCT, 'code': '360037004', 'display': 'Imaging - action (qualifier value)'}),
            'method': cc({'system': SCT, 'code': MPMRI_CODE,
                          'display': 'Multiparametric magnetic resonance imaging'}),
            'bodySite': cc({'system': SCT, 'code': '41216001',
                            'display': 'Prostatic structure (body structure)'}),
            'subject': patient_ref,
        }
        when = effective(mpmri[-1])
        if when:
            imaging_obs['effectiveDateTime'] = when
        imaging_obs = ctx.append(imaging_obs, 'imaging-mpmri')
        stats['imaging'] += 1
    if tnm[CT_OBS]:
        stage_obs('stage-clinical',
                  [tnm[CT_OBS][0]] + tnm[CN_OBS][:1] + tnm[CM_OBS][:1],
                  [COMP_T, COMP_N, COMP_M],
                  CLINICAL_STAGING,
                  imaging_obs, 'cancer-stage-evidence-reference-imaging')
    if tnm[PT_OBS]:
        stage_obs('stage-pathological',
                  [tnm[PT_OBS][0]] + tnm[PN_OBS][:1],
                  [COMP_T, COMP_N],
                  PATHOLOGICAL_STAGING,
                  rp_procedures[0] if rp_procedures else None,
                  'cancer-stage-evidence-reference-surgery')

    # --- EpisodeOfCare: active surveillance ---
    for careplan in ctx.by_type.get('CarePlan', []):
        codings = []
        for activity in careplan.get('activity', []):
            codings.append(first_coding((activity.get('detail') or {}).get('code')))
        codings.append(first_coding(careplan.get('category', [{}])[0] if careplan.get('category') else {}))
        codings += [first_coding(c) for c in careplan.get('category', [])]
        if not any(c and c.get('code') == AS_CAREPLAN_CODE for c in codings):
            continue
        period = careplan.get('period', {})
        eoc = {
            'resourceType': 'EpisodeOfCare',
            'meta': {'profile': [profile('episode-of-care-surveillance-eu-ccm')]},
            'status': 'finished' if period.get('end') else 'active',
            'patient': patient_ref,
            'diagnosis': [{'condition': condition_ref}],
            'period': period or None,
        }
        eoc = {k: v for k, v in eoc.items() if v is not None}
        ctx.append(eoc, 'eoc-surveillance')
        stats['eoc-surveillance'] += 1
        break

    # --- EpisodeOfCare: radiotherapy ---
    ebrt = procedures_with_code(ctx, EBRT_CODES)
    if ebrt:
        start = effective(ebrt[0])
        end = (ebrt[-1].get('performedPeriod') or {}).get('end') or effective(ebrt[-1])
        eoc = {
            'resourceType': 'EpisodeOfCare',
            'meta': {'profile': [profile('episode-of-care-radiotherapy-eu-ccm')]},
            'status': 'finished',
            'patient': patient_ref,
            'diagnosis': [{'condition': condition_ref}],
            'period': {'start': start, 'end': end},
            'extension': [{'url': ext('radiotherapy-intent'),
                           'valueCodeableConcept': cc(PALLIATIVE if m1 else CURATIVE)},
                          # profile requires the body-site extension (1..1) alongside intent
                          {'url': ext('radiotherapy-body-site'),
                           'valueCodeableConcept': cc({'system': SCT, 'code': '41216001',
                                                       'display': 'Prostatic structure (body structure)'})}],
        }
        ctx.append(eoc, 'eoc-radiotherapy')
        stats['eoc-radiotherapy'] += 1

    # --- EpisodeOfCare: systemic treatment (ADT/ARPI/taxanes) ---
    systemic = []
    for mr in ctx.by_type.get('MedicationRequest', []):
        codings = ((mr.get('medicationCodeableConcept') or {}).get('coding', []))
        atc = {c.get('code') for c in codings if 'atc' in (c.get('system') or '').lower()}
        atc |= {c.get('code') for c in codings}
        if atc & (ADT_ATC | TAXANE_ATC):
            systemic.append((mr, bool(atc & TAXANE_ATC)))
    if systemic:
        systemic.sort(key=lambda pair: pair[0].get('authoredOn') or '')
        has_taxane = any(t for _, t in systemic)
        ongoing = any((pair[0].get('status') == 'active') for pair in systemic)
        eoc = {
            'resourceType': 'EpisodeOfCare',
            'meta': {'profile': [profile('episode-of-care-systematic-treatment-eu-ccm')]},
            'status': 'active' if ongoing else 'finished',
            'patient': patient_ref,
            'diagnosis': [{'condition': condition_ref}],
            'period': {'start': systemic[0][0].get('authoredOn')},
            'type': [cc({'system': SCT, 'code': '367336001', 'display': 'Chemotherapy (procedure)'}
                        if has_taxane else
                        {'system': SCT, 'code': '169413002', 'display': 'Hormone therapy (procedure)'})],
            'extension': [
                {'url': ext('systematic-treatemmt-intent'),  # sic - draft's slice name
                 'valueCodeableConcept': cc(PALLIATIVE if m1 else CURATIVE)},
                {'url': ext('systematic-treatemmt-ongoing'), 'valueBoolean': ongoing},
            ],
        }
        ctx.append(eoc, 'eoc-systemic')
        stats['eoc-systemic'] += 1

    # --- Clinical cancer progression (biochemical recurrence) ---
    for recurrence in ctx.by_type.get('Condition', []):
        coding = first_coding(recurrence.get('code'))
        if not coding or coding.get('code') != RECURRENT_CODE:
            continue
        progression = {
            'resourceType': 'Observation',
            'meta': {'profile': [profile('observation-clinical-cancer-progression-eu-ccm')]},
            'status': 'final',
            'code': cc({'system': LOINC, 'code': '97509-4', 'display': 'Cancer disease progression'}),
            'subject': patient_ref,
            'focus': [condition_ref],
            'valueCodeableConcept': cc({'system': SCT, 'code': '263853000',
                                        'display': 'Recurrent episode (qualifier value)'}),
            'extension': [{'url': ext('extent-type'),
                           'valueCodeableConcept': cc({'system': SCT, 'code': '255470001',
                                                       'display': 'Local (qualifier value)'})}],
        }
        if recurrence.get('onsetDateTime'):
            progression['effectiveDateTime'] = recurrence['onsetDateTime']
        ctx.append(progression, 'progression')
        stats['progression'] += 1
        break

    # --- Last follow-up ---
    deceased = ctx.patient.get('deceasedDateTime')
    encounter_ends = [(e.get('period') or {}).get('end') for e in ctx.by_type.get('Encounter', [])]
    last_contact = max([d for d in encounter_ends if d] or [None], default=None)
    when = deceased or last_contact
    if when:
        has_recurrence = any((first_coding(c.get('code')) or {}).get('code') == RECURRENT_CODE
                             for c in ctx.by_type.get('Condition', []))
        followup = {
            'resourceType': 'Observation',
            'meta': {'profile': [profile('observation-last-follow-up-eu-ccm')]},
            'status': 'final',
            'code': cc({'system': SCT, 'code': '413744002', 'display': 'Cancer screening follow up (finding)'}),
            'subject': patient_ref,
            'effectiveDateTime': when,
            'extension': [
                {'url': ext('vital-status'),
                 'valueCodeableConcept': cc({'system': SCT, 'code': '419099009', 'display': 'Dead (finding)'}
                                            if deceased else
                                            {'system': SCT, 'code': '438949009', 'display': 'Alive (finding)'})},
                {'url': ext('evidence-of-disease'), 'valueBoolean': bool(has_recurrence or m1)},
            ],
        }
        ctx.append(followup, 'last-follow-up')
        stats['last-follow-up'] += 1

    with open(path, 'w') as f:
        json.dump(bundle, f)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'synthea', 'output', 'fhir')
    parser.add_argument('fhir_dir', nargs='?', default=default_dir)
    parser.add_argument('--base', default='http://hl7.eu/fhir/cancer-common',
                        help='ECCDM canonical base URL (draft; may still change)')
    args = parser.parse_args()

    files = sorted(glob.glob(os.path.join(args.fhir_dir, '*.json')))
    if not files:
        print(f'no bundles in {args.fhir_dir}', file=sys.stderr)
        sys.exit(1)
    from collections import Counter
    stats = Counter()
    touched = 0
    for path in files:
        name = os.path.basename(path)
        if name.startswith(('hospitalInformation', 'practitionerInformation')):
            continue
        try:
            if process_bundle(path, args.base, stats):
                touched += 1
        except Exception as exc:
            print(f'ERROR {name}: {exc}', file=sys.stderr)
            raise
    print(f'scanned {len(files)} bundles | cancer bundles reshaped {touched}')
    for kind, count in sorted(stats.items()):
        print(f'  {kind}: {count}')


if __name__ == '__main__':
    main()
