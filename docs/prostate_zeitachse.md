# Prostata-Zeitachse — Evidenzrecherche (Stand 2026-09-02)

Recherche zur **temporalen Achse** des Prostata-Moduls. Adressiert:

- **`synpros-6n1`** — zeitabhängige Übergänge (Hazards) und kalibrierte Inter-Event-Dauern
- **`synthea-eu-cancer-bp2`** — GENIE BPC als Quelle für TTNT-/PFS-Verteilungen
- berührt **`synpros-6zm`** (risikoadaptierte Früherkennung) — die S3 2025 hat den Takt geändert

Konventionen wie in `epidemiology/prostate_calibration.md`: jeder Wert mit Quelle und
Confidence-Flag 🟢 (belastbar) / 🟡 (indikativ, Transfer nötig) / 🔴 (Prior, ersetzungsbedürftig).

---

## 0. Was diese Runde ändert — Kurzfassung

| # | Befund | Wirkung |
|---|---|---|
| **Z1** | **GENIE BPC ist für Prostata nicht mehr blockierend.** Die Frankfurter Kohorte (n=1.098, deutsch, publiziert) liefert genau die Linien-PFS/OS, die `bp2` erzeugen sollte. | `bp2` von *blockierend* auf *optionale Verfeinerung* herabstufen; Synapse-Registrierung ist kein Pfadhindernis mehr → §8 |
| **Z2** | **`mCRPC_Delay` (heute uniform 1–3 J) ist falsch parametrisiert.** mHSPC→mCRPC median **21 Monate** (95 % KI 19–23), nicht 24 Mo uniform — und die Verteilung ist rechtsschief, nicht flach. | §6.1 |
| **Z3** | **BCR-Prior 0,40 / 0,20 ist zu niedrig für Hochrisiko und zu hoch für Niedrigrisiko.** Gemessen (post-2010, 8 J): niedrig 21 %, günstig-intermediär 25 %, ungünstig-intermediär 41 %, hoch 60 %. | ersetzt die 🔴-Priors in `prostate_calibration.md` §10 → §4.2 |
| **Z4** | **Zeit bis BCR ist analytisch fassbar**: median 2,5 J (IQR 0,9–5,5) → Lognormal μ=0,916 σ=1,342. Die Hazardform ist inzwischen **gemessen** (Walz 2009, Volltext, zwei Kohorten): **k hängt von der Risikogruppe ab** — 0,85 intermediär, 0,55 hoch. | §4.1, **§4.3 (2. Runde)** |
| **Z5** | **Salvage ist PSA-getriggert, nicht zeit-getriggert.** 79,4 % der deutschen Zentrumspatienten starten die SRT bei PSA < 0,5 ng/ml. Der Delay BCR→Salvage ist damit kurz und aus der Nachsorge-Taktung emergent. | §5.1 |
| **Z6** | **Die S3 2025 hat den Früherkennungs-Takt neu definiert** (PSA-Basiswert ab 45; <1,5 → ≥5 J, 1,5–3,0 → 2 J, ≥3,0 → Abklärung mit Bestätigung binnen 3 Monaten). Das ist eine *Zeitschicht*, die das Modul heute gar nicht hat. | §1.1 |
| **Z7** | **Für Deutschland gibt es keine Wartezeit-Kennzahl.** Der DKG/OnkoZert-Kennzahlenbogen Prostata (Kennzahlen 1a–22) enthält **keine einzige Zeitgröße** — verifiziert durch Volltextlesung des Jahresberichts 2024. | echte Datenlücke → §2.3 |
| **Z8** | **Überlebens-Anker weichen ab**: `prostate_calibration.md` §5 nennt 5-/10-J-RS 93,3 % / 90,7 %; RKI „Krebs in Deutschland" (Datenbasis 2017–2018) nennt **89 % / 88 %**. | Anker vereinheitlichen → §7.2 |

---

# Teil 1 — Die Eintritts-Uhr (Früherkennung)

## 1.1 Der neue S3-Takt 2025 — eine Zeitschicht, die im Modul fehlt

Die aktualisierte S3-Leitlinie (Juli 2025, v8.x) ersetzt die bisherige „PSA auf Wunsch"-Logik durch
einen **risikoadaptierten Screening-Takt mit expliziten Intervallen**:

| Baseline-PSA (ab 45 J) | Nächste Messung | Populationsanteil | Conf |
|---|---|---|---|
| **< 1,5 ng/ml** | frühestens nach **5 Jahren** | ≈ 89 % der 45-Jährigen, ≈ 82 % der 50-Jährigen | 🟢 |
| **1,5–3,0 ng/ml** | alle **2 Jahre** | Rest | 🟢 |
| **≥ 3,0 ng/ml** | sofortige Abklärung | — | 🟢 |

Abklärungskette bei PSA ≥ 3,0:

1. **Bestätigungs-PSA innerhalb von 3 Monaten** 🟢
2. bleibt der bestätigte Wert > 3 ng/ml und ist nicht durch Prostatavolumen, akute Entzündung oder
   andere bekannte Ursachen erklärbar → **mpMRT** (kein Direkt-zur-Biopsie mehr) 🟢
3. **Biopsie** bei PI-RADS 4/5; PI-RADS 3 nur bei hohem Individualrisiko (**PSA-Dichte > 0,15**) 🟢

> **Modellierungs-Konsequenz.** Das Modul kennt heute nur `Symptom_Check` mit 0,12/Jahr als
> Durchsatz-Stellknopf. Der S3-Takt ist eine **zweite, parallele Eintrittsschiene** mit einer
> *eigenen Uhr* (5 J / 2 J / sofort). Für eine epidemiologisch repräsentative Kohorte ist das die
> realistischere Eintrittslogik; für die reine Test-Kohorte bleibt der Symptom-Trigger ausreichend.
> Direkt relevant für **`synpros-6zm`**.

Quelle: Dtsch Arztebl Int, „The Early Detection, Diagnostic Evaluation, and Local Treatment of
Prostate Cancer" (25.07.2025); Die Urologie, „Früherkennung des Prostatakarzinoms — Empfehlungen
der aktualisierten S3-Leitlinie 2025".

## 1.2 Altersabhängige Inzidenz — der Hazard hinter dem Eintritt

RKI/ZfKD „Krebs in Deutschland", ICD-10 C61, Datenbasis 2018 (Tabelle 3.22.2):

| Alter | Erkrankungsrisiko nächste 10 Jahre | „jemals" |
|---|---|---|
| 35 J | < 0,1 % (1 von 4.800) | 12,3 % |
| **45 J** | **0,4 %** (1 von 250) | 12,4 % |
| **55 J** | **2,3 %** (1 von 43) | 12,5 % |
| **65 J** | **5,6 %** (1 von 18) | 11,5 % |
| 75 J | 5,9 % (1 von 17) | 7,9 % |
| Lebenszeit | — | **12,1 %** (1 von 8) |

Daraus die mittlere Jahres-Hazard im Kohortenfenster: 🟢

- **45–55 J: ≈ 0,040 %/Jahr**
- **55–65 J: ≈ 0,233 %/Jahr**
- Steigerungsfaktor über die Dekade: **≈ 5,8×**

> **Modellierungs-Konsequenz.** Punkt A(3) aus `6n1` („altersabhängige Präsentation 50→60→70")
> ist damit quantifiziert: eine geometrische Steigerung von rund **1,19×/Jahr** bildet den
> Faktor 5,8 über 10 Jahre ab. Das ersetzt die 100-%-symptomatisch-Vereinfachung für den
> repräsentativen Lauf.

Weitere Anker derselben Quelle: 65.200 Neuerkrankungen (2018), rohe Rate 159,4/100.000,
standardisiert 99,1; **mittleres Erkrankungsalter 71–72 Jahre**; mittleres Sterbealter 80 J.

---

# Teil 2 — Prozesszeiten der Diagnostikkette

## 2.1 Der belastbarste Zeitraster: polnischer Fast-Track (bereits in den Bead-Notes)

Sierocka et al. 2025, *Cancers* 17:1842 (PMC12153762), n = 6.661 C61-Patienten, 60.510 Termine,
ein großes polnisches Onkologiezentrum, 2018–2022, DiLO-Fast-Track: 🟡 *(Transfer PL→DE)*

| Prozessschritt | gemessen (Median, Tage) | DiLO-Sollwert |
|---|---|---|
| Hausarzt → Basisdiagnostik | **19,6** | 28 |
| Facharzt → vertiefte Diagnostik | **27,7** | 21 |
| Tumorkonferenz (Concilium) | **14,0** | 14 |
| Konferenz → Therapiebeginn | **18,3** | 14 |
| Abstand Folgetermine (Follow-up) | **56,3** | — |

**42 % Fristverletzungen** insgesamt; am stärksten beim Therapiebeginn (53 %) und beim Abschluss
der Diagnostik (37 %). Die Streuung ist damit ein *Modellmerkmal*, keine Störung.

## 2.2 Internationale Vergleichswerte

| Intervall | Wert | Quelle | Conf |
|---|---|---|---|
| Diagnose → Therapiebeginn (gesamt, US) | **median 71 d** (IQR 43–107) | US-Kohortenanalysen zur *time to treatment initiation* | 🟡 |
| Diagnose → ADT-Start | median **36 d** | dito | 🟡 |
| Diagnose → EBRT-Start | median **63 d** | dito | 🟡 |
| **Biopsie → radikale Prostatektomie** | **median 77 d** (IQR 55–107), n = 6.202, 2011–2020 | Tertiärzentrum-Kohorte (World J Urol 2024) | 🟢 |
| Biopsie → RP (zweite Serie) | median **83 d** (Range 61–109) | Multi-Surgeon-Datenbank | 🟡 |
| Diagnostisches Intervall Prostata (NL) | **median 137 d** — längstes unter fünf häufigen Krebsarten | Eur J Cancer, NL-Registerdaten | 🟡 |

> Der Kontrast NL 137 d ↔ PL ~80 d ↔ US 71 d ist selbst ein Ergebnis: **die Prozesszeit ist die am
> stärksten systemabhängige Größe im ganzen Modul.** Sie gehört deshalb in
> `epidemiology/countries.yaml`, nicht hart ins Modul.

## 2.3 Die deutsche Lücke — ein Negativbefund mit Belegkraft

Der **Jahresbericht der zertifizierten Prostatakrebszentren (DKG/OnkoZert), Kennzahlenauswertung
2024** (Auditjahr 2023, Kennzahlenjahr 2022; 163 Standorte, 41.374 Primärfälle) wurde vollständig
gelesen. Die Kennzahlen 1a bis 22 umfassen Fallzahlen, Konferenzvorstellung, AS-Anteil,
Therapieanteile, Befundberichte, Komplikationen, Nebenwirkungen — **aber keine einzige Zeit- oder
Wartezeit-Kennzahl.** 🟢 *(Negativbefund, primärquellengeprüft)*

**Konsequenz:** für Deutschland existiert kein publizierter Zeitanker für Diagnose→Therapie.
Empfehlung: den polnischen Fast-Track-Raster als Basis nehmen und über `countries.yaml`
skalieren; die deutschen Werte als 🔴 kennzeichnen, bis eine Registerauswertung vorliegt.

## 2.4 Vorschlag: Verteilungen statt fixer Delays

Prozesszeiten sind rechtsschief mit langem Schwanz (42 % Fristüberschreitung) — also
**Lognormal**, nicht Uniform. Parametrisierung aus Median + geschätzter IQR:

| Segment | Median | vorgeschlagene Verteilung | Conf |
|---|---|---|---|
| Auffälliger PSA → Bestätigungs-PSA | 30 d | Lognormal(ln 30; σ≈0,5), gekappt bei 90 d (S3-Frist) | 🟡 |
| Bestätigung → mpMRT | 21 d | Lognormal(ln 21; σ≈0,6) | 🔴 |
| mpMRT → Biopsie | 21 d | Lognormal(ln 21; σ≈0,6) | 🔴 |
| Biopsie → Befund/Diagnose | 10 d | Lognormal(ln 10; σ≈0,4) | 🔴 |
| Diagnose → Tumorkonferenz | 14 d | aus Sierocka | 🟡 |
| Konferenz → RP | 60 d | so, dass Biopsie→RP ≈ 77 d Median trifft | 🟢 (Ziel-Anker) |
| Konferenz → RT-Start | 45 d | US-EBRT 63 d ab Diagnose | 🟡 |
| Konferenz → ADT-Start | 14 d | US-ADT 36 d ab Diagnose | 🟡 |
| Konferenz → AS-Eintritt | 0–14 d | AS braucht keinen Slot | 🟡 |

**Validierungsanker für den generierten Lauf:** Biopsie→RP soll median ≈ 77 d mit IQR ≈ 55–107 d
ergeben; Diagnose→jede Therapie median ≈ 71 d.

---

# Teil 3 — Active Surveillance als Hazard statt als 50-%-Klumpen

## 3.1 Vier unabhängige Konversionskurven

| Kohorte | 1 J | 2 J | 3 J | 5 J | 10 J | 15 J | Conf |
|---|---|---|---|---|---|---|---|
| **Johns Hopkins** (n≈1.300, very-low/low risk) — interventionsfrei | — | **81 %** | — | **59 %** | **41 %** | — | 🟢 |
| **PRIAS** — AS-Persistenz | 89 % | **77,3 %** | — | 48–55 % | **27 %** | — | 🟢 |
| **HAROW** (DE, community) | — | — | — | ≈ 50 % konvertiert | interventionsfrei **33,8–34,6 %** | — | 🟢 |
| **ProtecT** (RCT, Active Monitoring) | — | — | — | — | — | **61 % radikal behandelt** | 🟢 |
| **GAP3** — 3-J treatment-free nach MRT-Status | — | — | 80 % (MRT unauffällig) / **63 %** (MRT suspekt) | — | — | — | 🟢 |

Ergänzend Johns Hopkins: kumulative **Grade-Reklassifikation** 21 % / 30 % / 32 % bei 5 / 10 / 15 J;
kumulative **kurative Intervention** 50 % @10 J, 57 % @15 J; mediane behandlungsfreie Zeit **8,5 J**.
PRIAS-Abbruchgründe nach 10 J: **41 % protokollbasierte Reklassifikation**, 5 % Angst/Patientenwunsch.

> **Der alte 0,50-Wert bleibt bestätigt.** Fünf-Jahres-Konversion: JHU 41 %, PRIAS 45–52 %,
> HAROW ≈ 50 %. `AS_Progression_Branch = 0.50` in `prostate_calibration.md` §4 ist korrekt —
> aber als *Punktwert* verliert er die Form der Kurve.

## 3.2 Weibull-Fits (selbst gerechnet, kleinste Quadrate auf S(t))

**Johns-Hopkins-Fit** (Anker 2/5/10 J): **λ = 11,14 Jahre, k = 0,867** — Residuen ≤ 0,018.
**PRIAS-Fit** (Anker 1/2/5/10 J): λ = 7,63 Jahre, k = 1,025 (praktisch exponentiell, aggressiveres
Protokoll mit engeren Reklassifikations-Kriterien).

Empfehlung: **JHU-Fit** als Basis (k < 1, front-loaded), PRIAS als Sensitivitäts-Variante.

Daraus die Jahres-Hazards und die per-Visit-Wahrscheinlichkeiten:

| Jahr | h(Jahr) | P je 6-Monats-Visite | P je 12-Monats-Visite |
|---|---|---|---|
| 1 | 12,37 % | 0,0656 | 0,1164 |
| 2 | 10,19 % | 0,0508 | 0,0969 |
| 3 | 9,51 % | 0,0470 | 0,0907 |
| 4 | 9,09 % | 0,0448 | 0,0869 |
| 5 | 8,79 % | 0,0433 | 0,0841 |
| 6 | 8,55 % | 0,0421 | 0,0820 |
| 7 | 8,37 % | 0,0412 | 0,0803 |
| 8 | 8,21 % | 0,0404 | 0,0788 |
| 9 | 8,07 % | 0,0397 | 0,0775 |
| 10 | 7,95 % | 0,0391 | 0,0764 |

Gegenprobe zu HAROW: der Fit sagt mediane Zeit bis Intervention ≈ 7,5 J bei den bis dahin
Konvertierten; HAROW misst median 33 Mo (RP) / 38,5 Mo (RT) **unter den Konvertierten** — beides
verträglich, weil HAROW nur die Konvertierten mittelt. 🟡

## 3.3 Der S3-2025-Überwachungstakt — daran hängt der per-Visit-Hazard

| Element | Takt | Conf |
|---|---|---|
| PSA bei **ISUP GG 1** | alle **6 Monate** | 🟢 |
| PSA bei **ISUP GG 2** (günstig) | alle **3 Monate** | 🟢 |
| **MRT-gestützte Re-Biopsie** | bei **12–18 Monaten** | 🟢 |
| AS-Abbruch | **nur bei histologischer Progression**, *nicht* bei PSA-Anstieg allein | 🟢 |

Neu in der S3 2025: AS ist auch für **ISUP GG 2 mit günstigem Risiko** vorgesehen
(< 25 % Gleason-Muster 4, kein kribriformes/intraduktales Wachstum); für GG 1 wird weder OP noch
Bestrahlung mehr empfohlen. Rund die Hälfte der lokalisierten Fälle qualifiziert sich.

> **Modellierungs-Konsequenz.** Die Reklassifikation wird *bei der Re-Biopsie entdeckt*, nicht
> kontinuierlich. Sauberste Umsetzung: Hazard über das Intervall akkumulieren, Ereignis aber erst
> am Biopsie-Termin (12–18 Mo, dann alle 2–3 J) manifestieren. Die PSA-Visiten erzeugen nur
> Observations, keine Zustandsübergänge — das entspricht exakt dem S3-Abbruchkriterium.

## 3.4 Deutscher AS-Anteil (DKG-Kennzahl 4, Kennzahlenjahr 2022) 🟢

- AS bei lokal begrenztem Niedrigrisiko-PCa: **32,83 %** aller so definierten Primärfälle
  (Zähler 2.192 / Nenner 6.677); Median der Zentrumsquoten 35,48 %; Anstieg 27,53 % (2018) → 35,48 % (2022)
- AS-Anteil an **allen** Primärfällen: **7,45 %** (2022), Watchful Waiting 2,29 %

---

# Teil 4 — Kurative Therapie → BCR als per-Visit-Hazard

## 4.1 Zeit bis BCR — direkt parametrisierbar

**Median 2,5 Jahre (IQR 0,9–5,5)** von RP bis BCR, n = 6.881 BCR-Patienten aus einer
Salvage-Naturverlaufs-Kohorte. 🟢
Konsistente Nebenwerte: median 2,9 J (PSA-Ära-Kohorte) 🟡; 30 Monate (laparoskopische RP) 🟡;
18,1 Monate (Einzelzentrum) 🟡.

**Lognormal-Fit aus Median + IQR** (eigene Rechnung): **μ = 0,9163, σ = 1,3418**

| Quantil | Jahre |
|---|---|
| p10 | 0,45 |
| p25 | 1,01 |
| **p50** | **2,50** |
| p75 | 6,18 |
| p90 | 13,96 |

→ **43,4 % der Rezidive innerhalb 2 Jahren**, 69,7 % innerhalb 5 Jahren, **30,3 % nach ≥ 5 Jahren.**

> Unabhängige Bestätigung: „27 % der biochemischen Versager traten nach ≥ 5 rezidivfreien Jahren
> auf" (Langzeit-Hazard-Analyse nach RP). Der Lognormal-Fit sagt 30,3 % — Abweichung 3 Prozentpunkte. 🟢

## 4.2 Kumulative BCR-Inzidenz nach Risikogruppe — ersetzt die 🔴-Priors

Zeitgenössische Kohorte (n = 6.682; davon 3.190 post-2010, medianes Follow-up 3,5 J):

| Risikogruppe (NCCN) | BCR @ 8 Jahre | bisheriger Modul-Prior |
|---|---|---|
| **niedrig** | **21 %** (16–25) | 0,20 (low/int, 10 J) 🔴 |
| **günstig intermediär** | **25 %** (20–30) | 0,20 🔴 |
| **ungünstig intermediär** | **41 %** (37–46) | 0,20 🔴 |
| **hoch** | **60 %** (56–64) | 0,40 (high, 10 J) 🔴 |

Gesamtkurve post-2010: **3 J 28 %, 5 J 33 %, 8 J 40 %.** 🟢
Historischer Quervergleich (D'Amico, ältere Kohorte, 15 J): niedrig 16 %, intermediär 30 %, hoch 46 % 🟡
— die neueren Zahlen liegen höher, weil sich der Case-Mix verschoben hat (Niedrigrisiko wandert in AS ab).

> **Korrektur:** Der Modul-Prior unterschätzt Hochrisiko deutlich (0,40 vs. 0,60 @8 J) und
> differenziert intermediär nicht in günstig/ungünstig — der Sprung 25 % → 41 % ist aber der
> größte Einzelunterschied in der ganzen Tabelle. **Die Aufteilung des intermediären Arms in
> günstig/ungünstig ist damit keine Kosmetik, sondern der Haupthebel.**

## 4.3 Die Hazardform — jetzt gemessen statt geschätzt

**Nachtrag 2026-09-02 (zweite Runde, Volltext beschafft).** Walz J., Chun F.K.H., Klein E.A.,
Reuther A., Graefen M., Huland H., Karakiewicz P.I., *Eur Urol* 2009;55:412–421,
DOI 10.1016/j.eururo.2008.11.005 — **Volltext gelesen.** Damit ist Lücke L2 geschlossen: die
jährlichen Hazardraten liegen jetzt Jahr für Jahr und für **zwei unabhängige Kohorten** vor.

### 4.3.1 Die Originaldaten

Zwei Kohorten: **Hamburg (n = 2.911, 1992–2005)** und **Cleveland Clinic (n = 2.875, 1987–2005)**.
Kein Patient erhielt adjuvante Therapie vor BCR. Nachsorge: q3 Mo im ersten Jahr, halbjährlich
Jahr 2–5, danach jährlich.

Die drei Risikogruppen sind **Walz-eigene, kombiniert klinisch-pathologische** Gruppen — *nicht*
NCCN und *nicht* D'Amico: 🟢

| Gruppe | Definition | Anteil |
|---|---|---|
| **niedrig** | PSA < 11 ng/ml **und** cT1c **und** pathologischer Gleason < 6 **und** negative Schnittränder **und** organbegrenzt | 23,7 % |
| **hoch** | PSA > 22 ng/ml **oder** Samenblaseninfiltration **oder** pathologischer Gleason > 8 **oder** Lymphknotenbefall **oder** cT3 | 18,9 % |
| **intermediär** | alle übrigen | 57,4 % |

**Annual hazard rate (anHR, % pro Jahr), Tabellen 3 und 4:** 🟢

| Jahr nach RP | HH niedrig | HH intermediär | HH hoch | CC niedrig | CC intermediär | CC hoch |
|---|---|---|---|---|---|---|
| 0–1 | 2,6 | 6,0 | **31,8** | 0,6 | 3,7 | **30,0** |
| 1–2 | 1,5 | 6,2 | 22,3 | 0,3 | 4,0 | 13,2 |
| 2–3 | 0,3 | 4,8 | 27,0 | 0,7 | 3,2 | 15,0 |
| 3–4 | 0,5 | 4,2 | 22,7 | 1,3 | 2,9 | 10,7 |
| 4–5 | 1,6 | 2,8 | 19,2 | 0,6 | 3,0 | 7,2 |
| 5–6 | 0 | 7,2 | 13,1 | 0,7 | 3,0 | 9,1 |
| 6–7 | 0 | 5,1 | 13,3 | 0 | 2,1 | 7,5 |
| 7–8 | 0 | 1,3 | 6,3 | 0 | 1,8 | 11,5 |
| 8–9 | 0 | 6,3 | 0 | 0 | 2,5 | 4,7 |
| 9–10 | 0 | 0 | 0 | 0 | 2,0 | 8,6 |
| **BCR-frei @10 J** | **93,7 %** | **64,5 %** | **20,9 %** | **96,0 %** | **75,5 %** | **30,8 %** |

> Die Nullen ab Jahr 6–8 in der Hamburger Kohorte sind **Kleinzahl-Artefakte** (bei Jahr 9–10 sind
> nur noch 1 bzw. 5 Patienten under risk). Für die Langzeitform ist die Cleveland-Kohorte
> maßgeblich, die bis Jahr 10 noch 37–249 Patienten hält.

### 4.3.2 Eigener Weibull-Fit an diese Daten

Fit von h(t) = (k/λ)(t/λ)^(k−1) an die anHR-Reihen, gewichtet mit √(Patienten at risk), nur Jahre
mit ≥ 30 Patienten at risk:

| Kohorte | Gruppe | λ (Jahre) | **k** |
|---|---|---|---|
| Hamburg | niedrig | 500 (Rand) | 0,554 |
| Cleveland | niedrig | 214,1 | **0,946** |
| Hamburg | intermediär | 23,07 | **0,871** |
| Cleveland | intermediär | 42,10 | **0,845** |
| Hamburg | hoch | 3,85 | 0,785 |
| Cleveland | hoch | 5,90 | **0,460** |

**Das zentrale Ergebnis: k ist keine Konstante, sondern hängt von der Risikogruppe ab.** 🟢

- **Intermediär: k ≈ 0,85** — und zwar in *beiden* Kohorten unabhängig (0,871 / 0,845). Die
  Hazard ist dort fast flach, nicht front-loaded.
- **Hoch: k ≈ 0,46–0,79** — steil abfallend, wie erwartet.
- **Niedrig:** Hazard so nahe an null, dass k schlecht identifiziert ist; die Kohorten
  widersprechen sich (0,55 vs. 0,95). Praktisch irrelevant, weil die absolute Rate < 1,5 %/Jahr liegt.

### 4.3.3 Validierung des bisherigen Modellwerts

Die erste Runde hatte **k = 0,55** über alle Gruppen gesetzt, kreuzvalidiert über die
Lognormal-Verteilung der Zeit-bis-BCR. Der Vergleich mit den echten Daten:

| Jahr | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Modell k = 0,55 (hoch)** | 29,2 | 13,5 | 10,7 | 9,2 | 8,2 | 7,5 | 6,9 | 6,5 | 6,1 | 5,8 |
| Walz Cleveland hoch | 30,0 | 13,2 | 15,0 | 10,7 | 7,2 | 9,1 | 7,5 | 11,5 | 4,7 | 8,6 |
| Walz Hamburg hoch | 31,8 | 22,3 | 27,0 | 22,7 | 19,2 | 13,1 | 13,3 | 6,3 | 0 | 0 |

**Für die Hochrisikogruppe trifft k = 0,55 die Cleveland-Kohorte fast punktgenau** (Jahr 1: 29,2
vs. 30,0; Jahr 2: 13,5 vs. 13,2) und liegt zwischen den beiden Kohorten. Das war Glück, aber es ist
belegtes Glück: 10-Jahres-BCR-freies Überleben Modell 35,5 % gegen Cleveland 30,8 %. ✅

**Für die intermediären Gruppen war k = 0,55 dagegen falsch** — beide Kohorten sagen ≈ 0,85. 🔴→🟢

### 4.3.4 Korrigierte Parametrisierung

Die Walz-Gruppen sind nicht NCCN-Gruppen, ihre λ sind also nicht übertragbar. Übertragbar ist die
**Form (k)**. Zuordnung über die Ereignisrate: Walz-„intermediär" (F(10) = 0,25–0,36) entspricht
etwa NCCN-niedrig/günstig-intermediär; Walz-„hoch" (F(10) = 0,69–0,79) entspricht NCCN-hoch.
Walz-„niedrig" (F(10) ≈ 0,05) ist eine pathologisch bestätigte Bestfall-Gruppe ohne NCCN-Pendant.

| Risikogruppe (NCCN) | F(8 J) | **k** | λ (Jahre) | F(1) | F(2) | F(3) | F(5) | F(10) | BCR-frei @10 J |
|---|---|---|---|---|---|---|---|---|---|
| niedrig | 0,21 | **0,85** | 43,80 | 0,039 | 0,070 | 0,097 | 0,146 | 0,248 | 75,2 % |
| günstig intermediär | 0,25 | **0,85** | 34,65 | 0,048 | 0,085 | 0,117 | 0,175 | 0,294 | 70,6 % |
| ungünstig intermediär | 0,41 | **0,70** | 19,94 | 0,116 | 0,181 | 0,233 | 0,316 | 0,460 | 54,0 % |
| hoch | 0,60 | **0,55** | 9,38 | 0,253 | 0,348 | 0,414 | 0,507 | 0,645 | 35,5 % |

Jährliche Hazard h(j) in % pro Jahr:

| Gruppe | J1 | J2 | J3 | J4 | J5 | J6 | J7 | J8 | J9 | J10 |
|---|---|---|---|---|---|---|---|---|---|---|
| niedrig | 4,0 | 3,2 | 3,0 | 2,8 | 2,7 | 2,6 | 2,6 | 2,5 | 2,5 | 2,4 |
| günstig intermediär | 4,9 | 3,9 | 3,6 | 3,5 | 3,3 | 3,2 | 3,2 | 3,1 | 3,0 | 3,0 |
| ungünstig intermediär | 12,3 | 7,7 | 6,6 | 5,9 | 5,5 | 5,2 | 4,9 | 4,7 | 4,5 | 4,4 |
| hoch | 29,2 | 13,5 | 10,7 | 9,2 | 8,2 | 7,5 | 6,9 | 6,5 | 6,1 | 5,8 |

> Plausibilitätsprüfung gegen Walz: die günstig-intermediäre Zeile (4,9 → 3,0 %/Jahr) liegt
> zwischen Walz-Cleveland-intermediär (3,7 → 2,0) und Walz-Hamburg-intermediär (6,0 → 6,3);
> die Hochrisiko-Zeile liegt zwischen den beiden Hochrisiko-Kohorten. ✅

### 4.3.5 Nebenbefund: Walz' eigener Nachsorge-Vorschlag

Tabelle 5 der Arbeit schlägt eine risikoadjustierte Nachsorge vor, die vom Leitlinien-Takt deutlich
abweicht: 🟢

| Jahr nach RP | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Leitlinie (Visiten/Jahr) | 3 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **hoch** | **6** | 4 | 3 | 2 | 2 | 2 | 2 | 1 | 1 | 1 |
| intermediär | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **niedrig** | **0** | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |

Für das Modul relevant, weil es zeigt, dass der **Nachsorgetakt selbst risikoabhängig sein könnte**.
Der S3-Takt (§4.4) bleibt aber die Referenz für den deutschen Kontext — der Walz-Vorschlag ist
ein Vorschlag geblieben, keine Leitlinienempfehlung.

## 4.4 Der S3-Nachsorgetakt und die daraus folgenden per-Visit-Wahrscheinlichkeiten

S3-Nachsorge nach kurativer Therapie (unverändert gegenüber v6/v8): 🟢
**erste Kontrolle innerhalb 12 Wochen**, dann **q3 Monate in Jahr 1–2**, **q6 Monate in Jahr 3–4**,
**jährlich ab Jahr 5**. BCR-Definition: post-RP PSA > 0,2 ng/ml zweimalig; post-RT Nadir + 2 (Phoenix).

**Das ist die Umsetzung von `6n1`: BCR als per-Visit-Hazard.** Statt eines Uniform-Draws bekommt
jede Nachsorgevisite die Wahrscheinlichkeit, dass zwischen letzter und aktueller Visite ein BCR
eingetreten ist — die Zeit-bis-BCR wird damit **emergent**:

| Visite (Ende, Jahre) | Intervall | niedrig | günstig int. | ungünstig int. | hoch |
|---|---|---|---|---|---|
| 0,25 | 3 Mo | 0,0123 | 0,0150 | 0,0456 | 0,1273 |
| 0,50 | 3 Mo | 0,0099 | 0,0121 | 0,0287 | 0,0613 |
| 0,75 | 3 Mo | 0,0091 | 0,0112 | 0,0246 | 0,0486 |
| 1,00 | 3 Mo | 0,0087 | 0,0106 | 0,0222 | 0,0418 |
| 1,25 | 3 Mo | 0,0084 | 0,0102 | 0,0206 | 0,0374 |
| 1,50 | 3 Mo | 0,0081 | 0,0099 | 0,0194 | 0,0342 |
| 1,75 | 3 Mo | 0,0079 | 0,0097 | 0,0185 | 0,0318 |
| 2,00 | 3 Mo | 0,0078 | 0,0095 | 0,0177 | 0,0298 |
| 2,50 | 6 Mo | 0,0150 | 0,0183 | 0,0332 | 0,0543 |
| 3,00 | 6 Mo | 0,0146 | 0,0178 | 0,0313 | 0,0497 |
| 3,50 | 6 Mo | 0,0142 | 0,0173 | 0,0298 | 0,0462 |
| 4,00 | 6 Mo | 0,0139 | 0,0170 | 0,0286 | 0,0433 |
| 5,00 | 12 Mo | 0,0269 | 0,0328 | 0,0534 | 0,0785 |
| 6,00 | 12 Mo | 0,0262 | 0,0318 | 0,0504 | 0,0719 |
| 7,00 | 12 Mo | 0,0255 | 0,0310 | 0,0480 | 0,0669 |
| 8,00 | 12 Mo | 0,0250 | 0,0304 | 0,0460 | 0,0628 |
| 9,00 | 12 Mo | 0,0245 | 0,0298 | 0,0443 | 0,0595 |
| 10,00 | 12 Mo | 0,0241 | 0,0294 | 0,0429 | 0,0567 |

*(Werte mit den gruppenspezifischen k aus §4.3.4; die erste Fassung dieses Dokuments hatte
k = 0,55 durchgängig und überzeichnete damit die Frühlast der intermediären Gruppen.)*

> **Der erste Balken ist der wichtigste.** Bei Hochrisiko fällt 12,7 % der gesamten
> BCR-Wahrscheinlichkeit auf die *erste* Nachsorgevisite nach 3 Monaten. Das ist kein Artefakt der
> Weibull, sondern reflektiert die persistierenden PSA-Werte nach RP, die klinisch als „frühes
> Rezidiv" imponieren. Wer das nicht will, sollte einen separaten Zustand
> *PSA-Persistenz* (nie unter 0,1 gefallen) modellieren und ihn aus dem BCR-Hazard herausrechnen.
> Vorschlag: eigenes Issue. 🟡

## 4.5 Post-RT-Verlauf

Für den RT-Arm gilt die Phoenix-Definition (Nadir + 2). Die Zeitachse ist dort **systematisch
länger**, weil der PSA-Nadir erst über 18–36 Monate erreicht wird; publizierte Median-Zeiten bis
zum biochemischen Versagen fehlen fast durchgängig, weil moderne Serien zu wenige Ereignisse
haben (z. B. 5-/9-Jahres-BF-freie Raten 92,1 % / 87,5 % bei n = 1.831, medianes Follow-up 71 Mo). 🔴

**Pragmatischer Vorschlag:** dieselbe Weibull, aber mit einer **Verschiebung von 12 Monaten**
(kein BCR vor Erreichen des Nadirs) und λ um 25 % gestreckt. Als 🔴 kennzeichnen.

---

# Teil 5 — BCR → Salvage → Metastasierung

## 5.1 Der Salvage-Trigger ist PSA-basiert, nicht zeit-basiert

**DKG-Kennzahl 16 „Beginn Salvage-Radiotherapie bei rezidiviertem PCa" (Kennzahlenjahr 2022):** 🟢

- Nenner: Patienten mit Z. n. RPE **und** PSA-Rezidiv **und** SRT: **n = 2.209**
- Zähler: davon SRT-Beginn **bei PSA < 0,5 ng/ml**: **n = 1.754**
- **Gesamtquote 79,40 %**; Median der Zentrumsquoten 81,48 %; Sollvorgabe ≥ 70 %, erfüllt von 83,9 % der Zentren
- Begründung der 23 Zentren, die die Vorgabe verfehlen: *verspätete Zuweisung durch externe Behandler (PSA ≥ 0,5)*

Ergänzend: medianer PSA-Wert bei SRT **0,50 ng/ml** (IQR 0,3–1,1) in einer gepoolten
Multizenter-Analyse (n = 2.460, 10 Zentren). 🟢

> **Modellierungs-Konsequenz.** Kein eigener `Delay`-Zustand mit Uniform-Draw. Sobald der BCR an
> einer Nachsorgevisite manifestiert (PSA > 0,2 ×2), wird die Salvage-RT beim **nächsten
> Termin ~4–8 Wochen später** ausgelöst — in **~80 % der Fälle bei PSA < 0,5**, in ~20 % verzögert.
> Der Delay ist damit vollständig aus der Nachsorge-Taktung emergent und braucht nur noch
> eine binäre „verspätete Zuweisung"-Verzweigung.

## 5.2 Metastasierung nach BCR — mit und ohne Salvage

Propensity-gematchte Salvage-Naturverlaufskohorte (n = 6.881 BCR, davon 2.109 je Arm gematcht,
medianes Follow-up nach BCR 10,2 J, 1.147 Metastasen-Ereignisse): 🟢

| Endpunkt | SRT behandelt | unbehandelt | NNT |
|---|---|---|---|
| Metastasen @ 5 J | **12,7 %** | **19,3 %** | 23 |
| Metastasen @ 15 J | **28,6 %** | **31,5 %** | 15 |
| PCa-spezifische Mortalität @ 5 J | 2,6 % | 5,2 % | — |
| PCa-spezifische Mortalität @ 15 J | 18,3 % | 23,0 % | — |

Historischer Naturverlaufs-Anker (Pound et al. 1999, Johns Hopkins, n = 304 BCR ohne frühe
Hormontherapie): **median 8 Jahre** vom PSA-Anstieg bis Metastasen; 34 % entwickelten Metastasen;
danach **median 5 Jahre** bis zum Tod. 🟡 *(Prä-Intensivierungs-Ära; Zeiten heute länger)*

Modifikator: **PSA-Verdopplungszeit < 9 Monate bei 23,3 %** einer post-RT-BCR-Kohorte (n = 1.663).
PSADT ist der stärkste Prädiktor für metastasenfreies Überleben. 🟡

> **Korrektur des Moduls.** `Salvage_Outcome → geheilt / Versagen = 0,55 / 0,45` bleibt als
> biochemischer Endpunkt vertretbar, aber der Ast „Versagen → metastasiert" darf **nicht sofort**
> feuern: nach SRT liegt die Metastasen-Kumulinzidenz bei nur 12,7 % nach 5 und 28,6 % nach 15 Jahren.
> Die Zeit BCR→Metastase gehört als eigener, sehr langsamer Hazard modelliert
> (Weibull mit λ ≈ 30 J, k ≈ 0,9 trifft 12,7/28,6 % näherungsweise). 🟡

---

# Teil 6 — Metastasierter Verlauf: die Linien-Zeitachse

## 6.1 mHSPC → mCRPC — ersetzt `mCRPC_Delay` uniform 1–3 Jahre

**Deutsche Primärquelle:** Universitätsklinikum Frankfurt, n = 1.098 metastasierte Patienten,
2013–2023, medianes Follow-up 32 Monate (IQR 11–60), medianes Alter bei Metastasierung 70 J
(IQR 64–76). 🟢

| Größe | Wert |
|---|---|
| **mHSPC → mCRPC (PFS)** | **median 21 Monate** (95 % KI 19–23) |
| **OS ab mHSPC** | **median 67 Monate** (95 % KI 62–77) |
| Mediane Anzahl Systemtherapielinien | **2** (IQR 2–4) |
| OS bei nur 1 Linie vs. ≥ 2 Linien | **26 vs. 52 Monate** |

Ergänzende Kontextwerte:

| Setting | Zeit bis Kastrationsresistenz | Conf |
|---|---|---|
| ADT-Monotherapie (historisch) | **7–12 Monate** | 🟡 |
| ADT + Docetaxel (Real World) | **17 Monate** | 🟡 |
| ADT + ARPI (Real World) | **30 Monate** | 🟡 |
| ADT + ARPI (Studien: TITAN/ARCHES/ENZAMET) | Median vielfach **nicht erreicht**, ~60 % ohne Kastrationsresistenz während Follow-up | 🟡 |

> **Konkrete Ersetzung.** `mCRPC_Delay` (heute `uniform 1–3 Jahre`, Mittel 24 Mo) wird zu einem
> **therapieabhängigen** Draw:
> - Arm *ADT + Docetaxel*: Lognormal mit Median **17 Mo**
> - Arm *ADT + ARPI*: Lognormal mit Median **30 Mo**
> - gewichtetes Mittel bei der Modul-Aufteilung 0,60 ARPI / 0,40 Docetaxel: **≈ 25 Mo** — nahe an den
>   21 Mo der Gesamtkohorte, die noch ADT-Mono-Anteile enthält. Das ist die interne Konsistenzprüfung.
> - σ ≈ 0,7 (rechtsschief; ~10 % erreichen die Kastrationsresistenz nie im Beobachtungsfenster)

## 6.2 mCRPC Linie für Linie 🟢

Frankfurt-Kohorte, 1. bis 6. Linie:

| Linie | median PFS | median OS ab Linienbeginn |
|---|---|---|
| **1.** | **11 Mo** | **47 Mo** |
| **2.** | **8 Mo** | **30 Mo** |
| **3.** | **7 Mo** | **24 Mo** |
| **4.** | **6 Mo** | **19 Mo** |
| **5.** | **7 Mo** | **17 Mo** |
| **6.** | **7 Mo** | **13 Mo** |

**Das ist genau das Zielprodukt von `bp2`** — nur aus einer deutschen statt einer US-Kohorte.

**Attrition** (Lübecker mCRPC-Kohorte, DE): ~**zwei Drittel** erreichen mindestens eine zweite
Therapielinie; der Anteil **halbiert sich bis zur dritten Linie**. 🟡

**Therapiedauern** (Patient-overview Prostate Cancer, NPCR Schweden): 🟢

| Substanz | chemonaiv | nach Docetaxel |
|---|---|---|
| Abirateron | **10,8 Mo** | 8,2 Mo |
| Enzalutamid | **14,1 Mo** | 11,1 Mo |

Docetaxel 1. Linie mCRPC (Lübeck): mittlere Dauer 4,7 Mo (SD 3,1), **Median 4,0 Mo** 🟡 —
entspricht etwa 6 Zyklen q3w bei teilweise vorzeitigem Abbruch.

**Therapieverteilung 1. Linie mCRPC, Wandel 2013 → 2023** (Frankfurt): 🟢
ADT-Monotherapie **31 % → 0 %**; Chemotherapie 16,7 % → 33,3 %; ARSI 42,9 % → 66,7 %.

> **Modellierungs-Konsequenz für `mCRPC_Branch`.** Der heutige 🔴-Prior „0,65 / 0,35 (nach 1–3 J)"
> wird ersetzt durch eine **Linien-Kaskade** mit expliziter Attrition: nach jeder Linie
> Progressionshazard (PFS oben) und konkurrierende Mortalität (OS oben); ~⅓ verlässt die Kaskade
> nach Linie 1, ~½ des Rests nach Linie 2. Die 47 → 13 Mo fallende OS je Linie ist die
> gesuchte „mit der Zeit steigende Sterbehazard" aus `6n1` A(2).

---

# Teil 7 — Kalenderbausteine und Validierungsanker

## 7.1 Therapiedauern als FHIR-Zeitspannen 🟢

| Baustein | Dauer | Quelle |
|---|---|---|
| EBRT normofraktioniert (74–80 Gy) | **≈ 8 Wochen** | S3 2025 |
| EBRT moderat hypofraktioniert (60 Gy / 20 Fx) | **4 Wochen** — heutiger Standard | CHHiP; S3 2025 |
| EBRT extrem hypofraktioniert | **5–7 Fraktionen über 1–2 Wochen** (intermediär, unter Bedingungen) | S3 2025 |
| ADT begleitend zur RT, **intermediäres** Risiko | **4–6 Monate** | S3 2025 |
| ADT begleitend zur RT, **hohes/sehr hohes** Risiko | **24–36 Monate** | S3 2025 |
| Docetaxel-Zyklus | 6 × q3w = **18 Wochen** (real oft 4 Mo, s. §6.2) | Standard |
| ARPI | kontinuierlich bis Progression (10,8–14,1 Mo, s. §6.2) | NPCR |

> Achtung: die S3-2025-ADT-Dauer bei hohem Risiko (24–36 Mo) ist **länger** als die in
> `prostate_calibration.md` §10 für Salvage genannten „6 oder 24 Monate" — das sind zwei
> verschiedene Indikationen (primäre RT vs. Salvage-RT) und dürfen nicht vermischt werden. 🟢

## 7.2 Überlebens-Validierungsanker — Diskrepanz auflösen

| Quelle | 5-J relatives Überleben | 10-J |
|---|---|---|
| RKI/ZfKD, „Krebs in Deutschland", Datenbasis 2017–2018 | **89 %** (89–91) | **88 %** (87–91) |
| in `prostate_calibration.md` §5 zitiert (PubMed 27208546) | 93,3 % | 90,7 % |

Absolute Überlebensraten derselben RKI-Quelle: 74 % (5 J) / 58 % (10 J).

> **Empfehlung:** RKI als kanonischen Anker führen (89 / 88 %), den älteren Wert als
> historische Referenz kennzeichnen. Ein 4-Prozentpunkte-Unterschied im 5-Jahres-RS verschiebt
> die Mortalitäts-Kalibrierung der Kohorte spürbar.

Weitere Anker: ProtecT 15-Jahres-PCa-spezifisches Überleben **96,6 % (AM) / 97,2 % (RP) / 97,7 % (RT)**,
kein signifikanter Unterschied (p = 0,53); Metastasenraten 9,4 % / 4,7 % / 5,0 %, entsprechend
**6,3 / 2,4 / 3,0 Ereignisse je 1.000 Personenjahre**. 🟢 — der beste verfügbare Anker für die
langfristige Metastasen-Hazard im lokalisierten Arm.

---

# Teil 8 — GENIE BPC: Prüfung für `bp2`

## 8.1 Was der Datensatz ist

**GENIE BPC Prostate v1.0-public** 🟢

| Merkmal | Wert |
|---|---|
| Fallzahl | **1.116** Patienten |
| Zentren | MSK, DFCI, VICC, UHN (3 × US, 1 × Kanada) |
| Genomische Sequenzierung | 2013–2018 (assoziiert mit GENIE v19.0-public) |
| Alter bei Sequenzierung | **37–88 Jahre** |
| Einschluss | OncoTree PRAD, Stadium I–IV, ≥ 2 Jahre mögliche Nachbeobachtung, Zufallsauswahl aus dem GENIE-Registry |
| Zugang | **Synapse `syn73719283`**; Teilmenge über `genie.cbioportal.org` |
| Phänomik | PRISSMM (Pathologie, Radiologie, Imaging, Signs/Symptoms, Tumormarker, Onkologen-Assessment) |

**Zugangsprüfung:** `genie.cbioportal.org` leitet auf Google-OAuth um — also **auch die
cBioPortal-Teilmenge ist nicht anonym zugänglich.** Es gibt keinen registrierungsfreien Weg. 🟢

## 8.2 Welche Zeitvariablen enthalten sind

Aus dem Analytic Data Guide (Volltext gelesen):

| Variable | Bedeutung |
|---|---|
| `tt_os_dx_days/_mos/_yrs` | OS ab Krebsdiagnose |
| `tt_os_d1_*` … `tt_os_d5_*` | OS ab Start des 1.–5. krebsgerichteten Medikaments |
| `pfs_i_adv_*`, `pfs_m_adv_*`, `pfs_i_or_m_adv_*`, `pfs_i_and_m_adv_*` | PFS ab Stadium-IV-Diagnose bzw. Fernmetastasen-Datum, vier PRISSMM-Definitionen (Bildgebung / Onkologen-Assessment / oder / und) |
| `tt_pfs_i_g_*` | PFS ab **Regimebeginn**, zensiert beim nächsten Regime |
| `regimen_number`, `regimen_number_within_cancer` | Linien-Nummerierung |
| `drugs_startdt_int_1` … `_5` | Startdatums-Intervalle je Substanz |

> **TTNT ist nicht vorberechnet** — es ist aus `regimen_number` + `drugs_startdt_int_*`
> selbst zu bilden. Machbar, aber es ist Eigenarbeit, keine Abfrage. 🟢

## 8.3 Warum es trotzdem nicht der beste Weg ist

1. **Selektionsbias, explizit im Guide benannt:** die Auswahl erfolgt über *sequenzierte* Patienten,
   und die Sequenzierung liegt nicht am Diagnosezeitpunkt → „may lead to several forms of bias …
   failure to [account for them] may result in incorrect inferences" (Verweis auf Brown et al. 2022). 🟢
2. **Redaktion:** Namen und Dauern von Prüfmedikamenten sowie Datumsintervalle, die auf
   ein Alter > 89 J schließen ließen, sind entfernt. 🟢
3. **Geografie:** rein nordamerikanische Zentren — für eine EU-Kohorte der schlechtere Anker.
4. **Der Ersatz ist besser:** §6.1/6.2 liefert Linien-PFS/OS aus einer **deutschen** Kohorte
   (n = 1.098) mit publizierten Medianen — genau die gesuchten Größen, ohne Registrierung,
   ohne Bias-Korrekturaufwand.

**Zwei Fundstücke am Rande, die festgehalten gehören:**

- Der **Prostata-Data-Guide (PDF) enthält an der Eligibility-Stelle „Aged 18-56 at the time of
  genomic sequencing"** — ein offensichtlicher Copy-Paste-Fehler aus dem Brustkrebs-Guide; die
  offizielle Datenseite nennt 37–88. Wer die Eligibility aus dem PDF zitiert, zitiert falsch. 🟢
- **GENIE BPC BrCa v1.0-public ist eine Early-Onset-Kohorte** (n = 1.130, Alter **18–56** bei
  Sequenzierung, MSK/DFCI/VICC, Guide veröffentlicht 12/2025). Für die Mamma-Kohorte **50–60**
  passt sie nur im schmalen Überlappungsband 50–56. Das war in `bp2` nicht bekannt. 🟢

## 8.4 Empfehlung für `bp2`

> **Neu skopen statt blockieren.** Prostata-Zeitverteilungen kommen aus §6; `bp2` wird zu einer
> optionalen Verfeinerung (P3) mit dem engeren Ziel „TTNT-Feinstruktur und Linien-Übergangsmatrix",
> und die Synapse-Registrierung verliert ihren Blocker-Status. Der Mamma-Teil von `bp2` braucht
> ohnehin eine eigene Bewertung wegen des Early-Onset-Zuschnitts.

---

# Teil 9 — Konkrete Modul-Änderungen (Arrow für Arrow)

| Modul-Element | heute | neu | Quelle | Conf |
|---|---|---|---|---|
| Eintritt (repräsentativer Lauf) | `Symptom_Check` 0,12/J, altersneutral | Jahres-Hazard × 1,19 je Lebensjahr (Faktor 5,8 über 45→65) | RKI 10-J-Risiken §1.2 | 🟢 |
| Früherkennungs-Takt | fehlt | S3-2025-Schleife: PSA <1,5 → 5 J, 1,5–3,0 → 2 J, ≥3,0 → Abklärung; Bestätigung ≤ 3 Mo | S3 2025 §1.1 | 🟢 |
| Workup-Delays | fix/uniform | Lognormal je Segment, Ziel-Anker Biopsie→RP median 77 d (IQR 55–107) | §2.2/2.4 | 🟡 |
| `AS_Progression_Branch` | 0,50 pauschal @5 J | Weibull λ = 11,14 J, k = 0,867; Ereignis nur an der Re-Biopsie (12–18 Mo, dann q2–3 J) | JHU-Fit §3.2/3.3 | 🟢 |
| AS-Monitoring | — | PSA q6 Mo (GG 1) / q3 Mo (GG 2); Abbruch nur bei histologischer Progression | S3 2025 §3.3 | 🟢 |
| `BCR_Check` (high) | 0,40 | Weibull **k = 0,55**, λ = 9,38 J → F(8) = 0,60; gegen Walz-Cleveland validiert | §4.2/4.3 | 🟢 |
| `BCR_Check` (low/int) | 0,20 | niedrig **k = 0,85** λ = 43,8 / günstig int. **k = 0,85** λ = 34,7 / **ungünstig int. k = 0,70** λ = 19,9 | §4.3.4 | 🟢 |
| BCR-Manifestation | Uniform-Draw | per-Visit-Hazard an der S3-Nachsorgekette (Tabelle §4.4) | §4.4 | 🟢 |
| Post-RT-BCR | wie post-RP | Weibull mit 12-Mo-Verschiebung, λ × 1,25 | §4.5 | 🔴 |
| BCR → Salvage | impliziter Delay | nächster Termin +4–8 Wo; 79,4 % bei PSA < 0,5, 20,6 % verspätet | DKG KZ 16 §5.1 | 🟢 |
| Salvage-Versagen → Metastase | sofort | eigener langsamer Hazard: 12,7 % @5 J / 28,6 % @15 J (mit SRT) | §5.2 | 🟢 |
| `mCRPC_Delay` | uniform 1–3 J | Lognormal, Median 17 Mo (Docetaxel-Arm) / 30 Mo (ARPI-Arm), σ ≈ 0,7 | §6.1 | 🟢 |
| `mCRPC_Branch` | 0,65 / 0,35 | Linien-Kaskade 1.–6. Linie mit PFS 11/8/7/6/7/7 Mo und OS 47/30/24/19/17/13 Mo | §6.2 | 🟢 |
| `mCRPC_Outcome_Branch` | 0,55 / 0,45 | ersetzt durch konkurrierende Mortalität je Linie | §6.2 | 🟢 |
| ADT-Dauer zur RT | 0,50 „ADT dazu" | intermediär 4–6 Mo, hoch 24–36 Mo | S3 2025 §7.1 | 🟢 |
| RT-Dauer | Punkt-Ereignis | 4 Wochen (moderat hypofraktioniert, Standard) bzw. 8 Wochen normofraktioniert | §7.1 | 🟢 |
| Überlebens-Anker | 93,3 / 90,7 % | **89 / 88 %** (RKI), 93,3/90,7 als historische Referenz | §7.2 | 🟢 |

---

# Teil 10 — Offene Lücken nach dieser Runde

| # | Lücke | Auswirkung | Nächster Schritt |
|---|---|---|---|
| L1 | **Keine deutschen Wartezeitdaten** (Diagnose→Therapie). DKG-Kennzahlenbogen enthält keine Zeitgröße. | Prozesszeiten bleiben PL/US-Transfer 🟡 | Klinische Krebsregister (LKR-Auswertung) anfragen oder als bewusste Setzung dokumentieren |
| ~~L2~~ | ~~Walz-Volltext nicht zugänglich~~ — **GESCHLOSSEN 2026-09-02** (Volltext über Charité-Zugang beschafft, §4.3). k ist jetzt gemessen und **gruppenspezifisch**: 0,85 (intermediär, beide Kohorten übereinstimmend), 0,55 (hoch, gegen Cleveland validiert). | k = 0,55 durchgängig war für die intermediären Gruppen zu niedrig → korrigiert 🟢 | erledigt |
| L3 | **Post-RT-BCR-Zeitverteilung** faktisch unpubliziert (zu wenige Ereignisse in modernen Serien) | RT-Arm bleibt 🔴 | Näherung dokumentieren; ggf. aus einer Brachytherapie-Serie mit langem Follow-up ableiten |
| L4 | **PSA-Persistenz nach RP** (nie unter 0,1 gefallen) ist im BCR-Hazard mitverbacken und erzeugt den auffälligen Erst-Visiten-Balken | verzerrt die frühe Zeitachse | eigenes Issue: separater Zustand *PSA-Persistenz* mit eigener Rate |
| L5 | **PSADT-Verteilung** nur als Anteil < 9 Mo (23,3 %) bekannt, keine volle Verteilung | Modifikator BCR→Metastase bleibt grob 🟡 | gezielte Suche nach einer Registerkohorte mit PSADT-Quantilen |
| L6 | **`countries.yaml` hat noch keine Zeitparameter** | Prozesszeiten sind derzeit hart | Feld `process_delays` je Land ergänzen (NL 137 d, PL ≈ 80 d, US 71 d als Startpunkte) |
| L7 | **Mamma-Teil von `bp2`** ist durch den Early-Onset-Zuschnitt der GENIE-BrCa-Kohorte fraglich | betrifft AP-M5/dba | eigene Bewertung, wenn das Mamma-Modul dran ist |
| L8 | **Kohorten-Heterogenität im Hochrisiko-Arm**: Walz-Hamburg und -Cleveland liefern bei identischer Gruppendefinition 10-Jahres-BCR-freies Überleben von 20,9 % vs. 30,8 % (k = 0,79 vs. 0,46). | die Hochrisiko-Form ist eine Bandbreite, kein Punkt 🟡 | als Sensitivitätsparameter führen (k ∈ [0,46; 0,79]), nicht als Fehler behandeln |

---

# Teil 11 — Quellenverzeichnis

**Leitlinien und Programme**

- S3-Leitlinie Prostatakarzinom, Version 8.x, Juli 2025 (Leitlinienprogramm Onkologie) — Früherkennungstakt, AS-Protokoll, Nachsorge, ADT-Dauern, Fraktionierung
- Deutsches Ärzteblatt International, „The Early Detection, Diagnostic Evaluation, and Local Treatment of Prostate Cancer", 25.07.2025 — englische Zusammenfassung der S3 2025 mit allen Intervallen
- Die Urologie (Springer), „Früherkennung des Prostatakarzinoms — Empfehlungen der aktualisierten S3-Leitlinie 2025", DOI 10.1007/s00120-026-02811-w

**Register und Qualitätsberichte**

- RKI/ZfKD, „Krebs in Deutschland", Kapitel 3.22 Prostata (ICD-10 C61), Datenbasis 2017–2018 — Inzidenz, altersabhängige 10-Jahres-Risiken, Überlebensraten
- DKG/OnkoZert, „Jahresbericht der zertifizierten Prostatakrebszentren — Kennzahlenauswertung 2024" (Auditjahr 2023, Kennzahlenjahr 2022) — AS-Anteil (KZ 4), Salvage-RT-Beginn (KZ 16), Therapieverteilung; **Negativbefund: keine Wartezeit-Kennzahl**

**Prozesszeiten**

- Sierocka A. et al., „An Analysis of Waiting Times for the Diagnosis and Treatment of Patients with Prostate Cancer …", *Cancers* 2025;17:1842 — PMC12153762
- World J Urol 2024, „Impact of the time interval between biopsy and radical prostatectomy on functional outcomes", DOI 10.1007/s00345-024-05324-3 — Biopsie→RP 77 d (IQR 55–107)
- Eur J Cancer, „Time to diagnosis and treatment for cancer patients in the Netherlands: Room for improvement?" — 137 d
- PLOS One 2019, „Time to initial cancer treatment in the United States and association with survival over time" — TTI 71 d

**Active Surveillance**

- Tosoian J.J. et al., „Intermediate and Longer-Term Outcomes From a Prospective Active-Surveillance Program for Favorable-Risk Prostate Cancer", *JCO* 2015;33:3379 — PMID 26324359
- Bokhorst L.P. et al., „A Decade of Active Surveillance in the PRIAS Study", *Eur Urol* 2016
- Herden J. et al., HAROW-Langzeitauswertung — PMC8332563
- Hamdy F.C. et al., ProtecT 15-Jahres-Ergebnisse, *NEJM* 2023 — PMC10704979
- Movember GAP3 Consortium, MRT-Status und Behandlungsfreiheit — *Eur Urol Open Sci*

**BCR, Salvage, Metastasierung**

- „Contemporary Risk of Biochemical Recurrence after Radical Prostatectomy in the Active Surveillance Era" — PMC11370885 / PMID 38490923 — BCR nach Risikogruppe, post-2010
- **Walz J., Chun F.K.H., Klein E.A., Reuther A., Graefen M., Huland H., Karakiewicz P.I., „Risk-adjusted hazard rates of biochemical recurrence for prostate cancer patients after radical prostatectomy", *Eur Urol* 2009;55:412–421 — PMID 19027223, DOI 10.1016/j.eururo.2008.11.005 — Volltext, Tabellen 3/4/5. Hauptquelle für die Hazardform in §4.3**
- „Understanding the Impact of Salvage Radiation on the Long-Term Natural History of Biochemically Recurrent Prostate Cancer After Radical Prostatectomy" — PMC12198693 — Zeit RP→BCR 2,5 J (IQR 0,9–5,5); Metastasen/PCSM mit und ohne SRT
- Pound C.R. et al., „Natural history of progression after PSA elevation following radical prostatectomy", *JAMA* 1999 — PMID 10235151
- „Risk-based Prostate-specific Antigen Monitoring Reduces Follow-up Burden After Radical Prostatectomy", 2025 — PMID 40328569

**Metastasierter Verlauf**

- „Contemporary Treatment Patterns and Oncological Outcomes of Metastatic Hormone-sensitive Prostate Cancer and First- to Sixth-line Metastatic Castration-resistant Prostate Cancer Patients", *Eur Urol Open Sci* 2024 — **PMC11260326** (Universitätsklinikum Frankfurt, n = 1.098) — **Hauptquelle für Teil 6**
- „Therapiesequenzen und -dauer beim mCRPC: eine retrospektive Aufarbeitung der Lübecker mCRPC-Kohorte", *Aktuelle Urologie* 2024 — PMID 38917849
- „Time on treatment with abiraterone and enzalutamide in the Patient-overview Prostate Cancer in the National Prostate Cancer Register of Sweden" — PMID 34533422

**GENIE BPC**

- AACR Project GENIE, „GENIE BPC Prostate v1.0-public Analytic Data Guide" (Statistical Coordinating Center, MSK), März 2026
- aacrprojectgenie.org/data/prostate-1-0-public/ — n = 1.116, Synapse `syn73719283`
- aacr.org/…/bpc/early-onset-brca/ — BrCa v1.0-public, n = 1.130, Alter 18–56
- Lavery J.A. et al., `{genieBPC}` R-Paket, *Bioinformatics* 2023;39:btac796

---

*Stand: 2026-09-02, zweite Runde (Walz-Volltext eingearbeitet, §4.3 neu, §4.4 neu gerechnet, L2 geschlossen).*

*Rechnungen (Weibull-/Lognormal-Fits, per-Visit-Tabellen) wurden für dieses Dokument selbst
durchgeführt (SciPy least_squares auf S(t) bzw. analytisch aus Median/IQR) und sind an den
jeweiligen Stellen mit Residuen bzw. Kreuzvalidierung ausgewiesen.*
