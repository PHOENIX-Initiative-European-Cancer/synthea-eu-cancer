# Time variance in the prostate module

> **Status (2026-09-08):** Das 2018–2022-Jahresfenster (§5, `Cohort_Year_Branch`/`Year_Lottery`)
> ist derzeit **deaktiviert** — Team-Entscheid: das Fenster enthält den COVID-Effekt und pinnt
> den Datensatz auf 2022. `Age_50_Guard` überspringt die Lotterie; alle Patienten nutzen die
> `_Other`-Varianten (5-Jahres-Durchschnitte) und behalten ihr natürliches Kalenderdatum.
> Reaktivierung: `Age_50_Guard.direct_transition` zurück auf `Cohort_Year_Branch` +
> `REFERENCE_DATE=20221231`. Zusätzlich wurde die Abklärungs-Wartezeit aus dem offenen
> Urologie-Encounter herausgelöst (eigener `Abklaerung_Encounter` nach dem Delay — sonst
> spannte ein ambulanter Encounter einen Monat auf).

This explains, in plain terms, how `modules/adult/prostate.json` now models
**realistic waiting times** between steps of the prostate-cancer pathway,
based on a real hospital study, instead of everything happening instantly.
It does **not** change any clinical odds (who gets diagnosed, which
treatment they get, survival) — only *when* things happen.

Source data: **Sierocka et al. 2025, *Cancers* 17:1842** — a 5-year study
(2018–2022) of prostate cancer patients at a large Polish hospital,
measuring how long patients actually waited between steps of care.
(https://doi.org/10.3390/cancers17111842)

---

## 1. The three new delays, built from the paper's data

The paper measured average waiting time (in days) for three steps, broken
down by year:

| Step | Delay's name in `prostate.json` | 2018 | 2019 | 2020 | 2021 | 2022 |
|---|---|---|---|---|---|---|
| Referral → first urology visit | `Initial_Diagnosis_Wait_*` | 12.8 | 17.6 | 21.3 | 21.0 | 24.4 |
| Elevated PSA → imaging/biopsy | `Comprehensive_Diagnostics_Wait_*` | 19.1 | 26.9 | 33.5 | 28.5 | 31.5 |
| Diagnosis confirmed → treatment starts | `Treatment_Scheduling_Delay_*` | 18.6 | 18.4 | 17.9 | 18.0 | 18.7 |

(The `*` stands for the year — e.g. `Initial_Diagnosis_Wait_2020` — plus an
`_Other` variant for patients outside 2018–2022, see §5.)

Two things worth noticing: **2020 is the slow year** for the two diagnostic
steps (plausibly COVID-related), while **the wait to start treatment barely
moved** — the hospital seems to have protected treatment capacity even when
diagnostics slowed down.

I added a `Delay` state at each of these three points in the pathway. Each
one doesn't just use the flat 5-year average — it picks a different wait
depending on which year the simulated patient is in, using the numbers
above. Patients diagnosed in a year we don't have data for (see §5) fall
back to the 5-year average.

**Why not just use the average number every time?** Because in real life,
no two patients wait *exactly* the average number of days — some wait a
lot less, some a lot more. So instead of a flat number, each delay is
drawn from a **Triangular distribution**: most patients land close to the
year's average, a few wait much less, a few wait much more — shaped like a
triangle when you plot how likely each wait length is (peak at the
average, tapering off toward a floor and a ceiling on either side).

---

## 2. The delays that already existed — what I changed

The module already had four waiting periods before this work — but they
used a **uniform** distribution: every day in the range was equally
likely, which isn't how real waiting times behave (see above). I kept
the same time ranges but changed the *shape* to Triangular, so waits
cluster around a realistic typical value instead of being flat-random:

| What it's waiting for | Delay's name in `prostate.json` | Range (unchanged) | Typical wait now (new) |
|---|---|---|---|
| Active surveillance → check if treatment is needed | `AS_Followup_Delay` | 1–5 years | ~3 years |
| First-line metastatic therapy → check for resistance | `mCRPC_Delay` | 1–3 years | ~1.5 years |
| Curative treatment → recurrence check | `PSA_Followup` | 1–4 years | ~2 years |
| Incidental cancer found during BPH surgery → follow-up visit | `Incidental_FollowUp_Delay` | 2–4 weeks | ~3 weeks |

Nothing about *when* these happen in the pathway changed — just how the
random wait time within that range is distributed.

---

## 3. How this looks in the code

Each delay is a small block like this one (the "referral → first visit"
wait, for a patient diagnosed in 2020):

```json
"Initial_Diagnosis_Wait_2020": {
  "type": "Delay",
  "unit": "days",
  "distribution": {
    "kind": "TRIANGULAR",
    "parameters": { "min": 5, "mode": 21.3, "max": 59 }
  },
  "direct_transition": "Urology_Encounter"
}
```

`mode` is the paper's actual number for that year; `min`/`max` are my own
estimate of a realistic floor and ceiling (the paper didn't report those).

Since the wait is different for each year, there's a small "router" step
right before each delay that checks which year the patient is in and
picks the matching block:

```
                    ┌─ year 2018 → wait ~13 days ─┐
                    ├─ year 2019 → wait ~18 days ─┤
patient reaches  ──►│ year 2020 → wait ~21 days ──├──► next step in the pathway
this point          ├─ year 2021 → wait ~21 days ─┤
                    └─ year 2022 → wait ~24 days ─┘
```

---

## 4. A patient's journey, with every delay marked

`⏱` = a waiting period; everything else is a clinical decision (unchanged
odds). Percentages are how many patients take that branch.

```
Symptoms start → ⏱ Initial_Diagnosis_Wait_* → visit + PSA test
```

**70% — PSA looks normal → BPH branch:** ultrasound → BPH diagnosed →
watchful waiting (33%) / medication (52%) / surgery (15%, of which 14%
incidentally finds cancer → ⏱ `Incidental_FollowUp_Delay` → joins the
cancer branch below).

**30% — PSA elevated → cancer work-up:**
```
⏱ Comprehensive_Diagnostics_Wait_* → ultrasound → MRI → biopsy → cancer confirmed
```
→ risk level assigned (Low 32% / Intermediate 34% / High 17% / Locally
advanced 11% / Metastatic 6%) →
```
⏱ Treatment_Scheduling_Delay_* →
```
- **Low risk:** active surveillance → ⏱ `AS_Followup_Delay` (years-long
  monitoring wait) → half stay stable, half eventually get treated
- **Intermediate / High / Locally advanced:** surgery or radiotherapy
  (± hormone therapy) → ⏱ `PSA_Followup` (recurrence-check wait) → most
  are cured; some recur → scan → salvage treatment
- **Metastatic:** hormone therapy + chemo → ⏱ `mCRPC_Delay` (wait to see
  if it stops working) → most respond to a second-line drug; some don't
  survive

---

## 5. Where the 2018–2022 dates come from

Since the paper's numbers are only for 2018–2022, most simulated patients
(85%, adjustable) are steered to have their pathway start in one of those
five years — weighted so 2018–2022 aren't equally likely either (this
weighting is currently a placeholder guess, since the paper didn't give
per-year patient *counts*, only wait *times*). The other 15% keep whatever
date they'd naturally have, so the dataset isn't 100% locked to 2018–2022.

One practical requirement: generating patients needs
`REFERENCE_DATE=20221231` set (see `scripts/run_cohort.sh`), otherwise some
patients can't be placed in the window correctly.

---

## 6. What's not modeled yet

The paper has more in it than I've used so far. In rough order of how much
they'd add:

- **Two more steps from the paper aren't in the pathway at all**: a
  "medical case conference" (tumor board, ~14 days wait) before treatment
  starts, and a "follow-up" step (~56 days between visits) after
  treatment. Both would be new states, not just new delays.
- **Repeat visits within a step aren't modeled.** The paper counts ~2
  appointments per patient for imaging/biopsy and ~3.8 for treatment
  (e.g. multiple radiotherapy sessions) — right now each step is just one
  wait followed by one instant action, not several separately-timed visits.
- **Real per-year patient volumes.** How many patients actually started in
  each of the 5 years is currently a guess (with a made-up dip for 2020) —
  swap in the real annual counts if you get them.
- **Real min/max spread per delay.** I estimated the floor and ceiling of
  each wait from the average alone; if you have actual shortest/longest
  observed waits (or a standard deviation), those would replace my guess.
- **Hospital length of stay isn't modeled** — the paper also measures how
  many days each *appointment itself* lasts (e.g. ~11 days for inpatient
  treatment), separate from the wait beforehand. Not represented yet.
- **Matching the paper's "missed the legal deadline" rates.** The paper
  found only 47% of patients started treatment within the legal 14-day
  limit. Right now the delay just has a realistic shape — it isn't tuned
  to reproduce that specific miss-rate.

---

## 7. If you want to change something

- A wait's typical length or spread → edit the `min`/`mode`/`max` numbers
  on the relevant `Delay` state in `modules/adult/prostate.json`.
- The 85%/15% "in the 2018–2022 window vs. not" split → `Cohort_Year_Branch`.
- The per-year weighting within the window → `Year_Lottery`.
