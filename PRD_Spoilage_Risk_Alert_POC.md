# PRD — Raw Material Quality & Spoilage Risk Alert System (POC)

**Author:** Juan Camilo Cárdenas Zabala  
**Date:** July 2026  
**Status:** Draft — Proof of Concept  
**Audience:** IT Chief Cesar

---

## 1. Background & problem statement

The company manufactures and distributes raw materials for the food and bakery industry. These materials are sensitive to storage conditions such as temperature, humidity, and time in storage. The project is intended to address the storage risks and alerts of flour, sugar, yeast, dairy powder and cocoa regarding temperature, relative humidity and storage time. These materials are stored in batches in higienic and hermetic boxes. Each batch contains all 5 materials, each box of 20 kg, so the batch weighs 100 kg.
All these affect quality and spoilage risk. Today, this monitoring is manual. Someone checks storage logs or Quality Control results and judges risk based on experience.

This creates two problems:
- **Reactive detection**: Quality issues are often caught after they've already affected a batch, rather than flagged early to avoid further issues.
- **Inconsistent judgment**: Risk assessment depends on who's reviewing the data and how much attention they have that day.

## 2. Main Objective of this POC

Demonstrate an automated pipeline that ingests batch storage data, evaluates spoilage/quality risk using an AI agent, and proactively alerts an administrator with a percentage risk score and a natural language explanation, so decisions can be made before a batch becomes unusable.

This is a proof of concept intended to demonstrate feasibility and value, not a production system as it is. It uses simulated data standing in for real sensor/ERP feeds.

## 2.1. Materials Optimal Factors

| # | Material | Temperature | Relative Humidity | Time stored |
|---|----------|-------------|-------------------|-------------|
| 1 | Flour | 10°C - 20°C | < 80% | 1 year |
| 2 | Sugar | 15°C - 25°C | < 65% | NO EXP |
| 3 | Yeast | 15°C - 25°C | < 60% | 1-2 year |
| 4 | Dairy Powder | 15°C - 20°C | < 60% | 1-2 year |
| 5 | Cocoa | 15°C - 20°C | < 50% | 2-3 year |

## 3. Objectives

- Show that raw material data can be automatically evaluated for quality risk
  without manual review.
- Produce risk scores that are **explainable** with reasoning,  so they're trustworthy enough to act on.
- Prove the architecture (n8n + AI agent) is realistic to extend with real company data, real sensors, and real notification channels later.

## 4. Target user

Plant/warehouse administrator or quality manager who currently reviews storage conditions and Quality Control data manually and decides what to prioritize, flag, or discard.

## 5. Scope

### 5.1 In scope (Phase 1 — core POC)

| # | Feature | Description |
|---|---------|--------------|
| 1 | Simulated batch data source | Mock dataset representing incoming batches. Each batch is a 100 kg hygienic, hermetic container holding five 20 kg boxes — one per material (flour, sugar, yeast, dairy powder, cocoa). Storage temp/humidity are tracked per batch (shared container conditions); days in storage is tracked per material box within the batch. |
| 2 | Scheduled/triggered ingestion | n8n workflow pulls new/updated batch records on a schedule (or manual trigger for demo purposes). |
| 3 | Preprocessing | Compute derived signals: deviation from ideal storage range per material type, age adjusted risk factors. |
| 4 | AI risk agent | LLM-based agent evaluates each batch against reference thresholds and returns a structured risk percentage, risk category (Risk 1 - Minimum, Risk 2 - Medium, Risk 3 - High), key contributing factors, and a recommended action. |
| 5 | Risk-based routing | Batches classified as **Risk 2 (35-69%)** or **Risk 3 (70-100%)** trigger an alert; all batches are logged regardless of risk category. |
| 6 | Alerting | Notification (Slack or email) sent to the administrator for high-risk batches, including the % score and reasoning. |
| 7 | Risk log / dashboard | All evaluated batches logged to a sheet/database with risk score and timestamp, enabling a simple visual history (e.g. conditional formatting by risk level). |

### 5.2 In scope (Phase 2 — stretch goal, if time allows)

| # | Feature | Description |
|---|---------|--------------|
| 8 | Conversational Q&A agent | A chat interface (n8n AI Agent with read access to the risk log) that lets the administrator ask questions about the data, like: "which material has the most high-risk batches this month?" or "show me every flour batch flagged in the last week." Reuses the same logged data from Phase 1; adds a query/retrieval tool rather than a new pipeline. |

### 5.3 Out of scope (for this POC)

- Integration with real IoT sensors or the company's actual ERP/QC systems
- Automated actions (e.g. auto-rejecting a batch, auto-notifying suppliers)
- User authentication, multi-tenant access, or permissions
- Production-grade error handling, retries, or SLAs
- Historical data migration or large-scale data volume testing

## 6. Risk scoring methodology

Section 2.1 defines the optimal temperature, humidity, and storage-time
ranges per material — that table is the sole source of truth the
preprocessing step and AI agent evaluate each batch against. No other input
factors (e.g. moisture content, supplier history) are used in this POC:
moisture would require a separate lab-sampling data source the company
doesn't currently capture in storage, and supplier history reflects
incoming quality risk rather than the storage-driven spoilage risk this
system is scoped to address.

The risk score is driven entirely by how far each material box's actual
conditions deviate from its row in 2.1:
- **Temperature deviation** — how far outside the ideal range, and by how much
- **Humidity deviation** — how far outside the ideal range, and by how much
- **Time in storage** — how close to, or past, the upper end of the material's
  storage-time range (sugar has no expiry, so this factor doesn't apply to it)

Implementation note: store the 2.1 table as a lookup object (JSON) in an n8n
Code node, keyed by material, and compute each material box's deviation from
its ideal range during preprocessing — so the AI agent reasons over
deviations (e.g. "4°C above ideal, 65% humidity vs 60% ideal, 340 days
stored vs a 365-day range") rather than raw numbers with no context.

### Risk Categories

The AI agent converts its evaluation into a **0-100 risk percentage**, which is then mapped into one of three operational categories.

| Risk Category | Risk % | Interpretation | Recommended Action |
|---|---|---|---|
| Risk 1 - Minimum | 0-34% | Storage conditions remain within acceptable operating limits. Minor deviations are unlikely to affect product quality. | Continue normal storage and monitoring. |
| Risk 2 - Medium | 35-69% | Storage conditions are approaching or moderately exceeding the recommended limits for one or more materials. | Send an alert, inspect the batch, and verify storage conditions. |
| Risk 3 - High | 70-100% | Significant deviation from the recommended storage conditions or storage duration. High likelihood of quality degradation or spoilage. | Send an immediate alert and perform a quality inspection before releasing or using the batch. |

The AI agent determines the percentage by evaluating the combined impact of temperature deviation, humidity deviation, and storage-time deviation described above. The percentage represents the overall probability of storage-related quality degradation for the batch.


## 7. Proposed architecture

Simulated batch data → Preprocessing → AI risk agent → Risk router → Alert (high risk) + Log (all batches)

- **Orchestration:** n8n
- **AI reasoning:** LLM agent using the Google Gemini API (free tier, no
credit card required), returning structured JSON:
risk_percentage, risk_category, key_factors, recommended_action.
Groq (free tier) is available as a fallback provider if Gemini's free-tier
rate limit is hit during a live demo — both are wired through n8n's AI
Agent node, so switching is a config change, not a rebuild.
- **Data store:** Google Sheets or Airtable (lightweight, visible, good for a
  live demo)
- **Alerting:** Slack or email node in n8n
- **(Phase 2) Q&A agent:** n8n AI Agent node with a "read rows" tool over the
  same data store

## 8. Success criteria for the demo

- E2E workflow runs live, from triggering a new batch to an alert
  landing in Slack/email, in under a few minutes.
- Risk scores are accompanied by a clear, human-readable explanation — not
  just a number.
- At least one "obviously high risk" and one "obviously low risk" simulated
  batch are included so the range of the system is visible.
- The log/dashboard shows a believable history (multiple batches, multiple
  materials, a visible trend).
- The chat agent correctly answers at least 2–3 sample questions about the logged data and won't answer unrelated questions.

## 9. Risks & open questions

- **Data realism:** Simulated data needs to be believable enough that the
  logic (thresholds, reasoning) looks like it would generalize to real
  company data. Worth basing ideal ranges on real published storage
  guidelines for each material where possible.
- **Threshold tuning:** What risk % should trigger an alert vs. just a log
  entry? For this proof of concept, the operational thresholds are:

| Risk Category | Risk % | Alert |
|---|---|---|
| Risk 1 - Minimum | 0-34% | No |
| Risk 2 - Medium | 35-69% | Yes |
| Risk 3 - High | 70-100% | Yes |

These thresholds can be calibrated later using historical production data once the system is connected to real operations.
- **Scope creep:** Phase 2 (chat agent) should only be attempted once Phase 1
  is fully working and demo-ready — it's an enhancement, not a dependency.

## 10. Timeline (suggested)

| # | Milestone | Target |
|---|---|---|
|1| Mock dataset + storage thresholds defined | Day 1–2 |
|2| Core n8n workflow (trigger → preprocess → AI agent → route) | Day 3–5 |
|3| Alerting + log/dashboard | Day 6–7 |
|4| End-to-end testing with varied scenarios | Day 8 |
|5| (Stretch) Chat Q&A agent | Day 9–10 |
|6| Demo polish & rehearsal | Day 11–12 |

## 11. Design

- **Colours**: On the dasboard - The main color is red #CF1D1D and the split complementaries are green #1DCF76 and blue #1D76CF. The color white #ffffff may be used for the background and big empty areas.

- **Frontend**: A dashboard with information about the risky batches and its explanations (database information). Also it should have the agent chat there. For the deployement Vercel may be a good option.
