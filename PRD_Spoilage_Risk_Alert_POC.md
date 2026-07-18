# PRD — Raw Material Quality & Spoilage Risk Alert System (POC)

**Author:** Juan Camilo Cárdenas Zabala  
**Date:** July 2026  
**Status:** Draft — Proof of Concept  
**Audience:** IT Chief Cesar

---

## 1. Background & problem statement

The company manufactures and distributes raw materials for the food and bakery industry (flour, sugar, yeast, dairy powders, oils, cocoa, etc.). These materials are sensitive to storage conditions such as temperature, humidity, and time in storage.
All these affect quality and spoilage risk. Today, this monitoring is manual. Someone checks storage logs or Quality Control results and judges risk based on experience.

This creates two problems:
- **Reactive detection**: Quality issues are often caught after they've already affected a batch, rather than flagged early to avoid further issues.
- **Inconsistent judgment**: Risk assessment depends on who's reviewing the data and how much attention they have that day.

## 2. Main Objective of this POC

Demonstrate an automated pipeline that ingests batch storage data, evaluates spoilage/quality risk using an AI agent, and proactively alerts an administrator with a percentage risk score and a natural language explanation, so decisions can be made before a batch becomes unusable.

This is a proof of concept intended to demonstrate feasibility and value, not a production system as it is. It uses simulated data standing in for real sensor/ERP feeds.

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
| 1 | Simulated batch data source | Mock dataset representing incoming raw material batches: material type, supplier, storage temp/humidity, days in storage, moisture %, supplier incident history. |
| 2 | Scheduled/triggered ingestion | n8n workflow pulls new/updated batch records on a schedule (or manual trigger for demo purposes). |
| 3 | Preprocessing | Compute derived signals: deviation from ideal storage range per material type, age adjusted risk factors. |
| 4 | AI risk agent | LLM-based agent evaluates each batch against reference thresholds and returns a structured risk percentage, risk level (low/medium/high), key contributing factors, and a recommended action. |
| 5 | Risk-based routing | Batches above a risk threshold trigger an alert; all batches are logged regardless of risk level. |
| 6 | Alerting | Notification (Slack or email) sent to the administrator for high-risk batches, including the % score and reasoning. |
| 7 | Risk log / dashboard | All evaluated batches logged to a sheet/database with risk score and timestamp, enabling a simple visual history (e.g. conditional formatting by risk level). |

### 5.2 In scope (Phase 2 — stretch goal, if time allows)

| # | Feature | Description |
|---|---------|--------------|
| 8 | Conversational Q&A agent | A chat interface (n8n AI Agent with read access to the risk log) that lets the administrator ask questions about the data, like: "which supplier has the most high riks batches this month?" or "show me every flour batch flagged in the last week." Reuses the same logged data from Phase 1; adds a query/retrieval tool rather than a new pipeline. |

### 5.3 Out of scope (for this POC)

- Integration with real IoT sensors or the company's actual ERP/QC systems
- Automated actions (e.g. auto-rejecting a batch, auto-notifying suppliers)
- User authentication, multi-tenant access, or permissions
- Production-grade error handling, retries, or SLAs
- Historical data migration or large-scale data volume testing

## 6. Proposed architecture

Simulated batch data → Preprocessing → AI risk agent → Risk router → Alert (high risk) + Log (all batches)

- **Orchestration:** n8n
- **AI reasoning:** LLM agent (Claude via API), returning structured JSON:
  `risk_percentage`, `risk_level`, `key_factors`, `recommended_action`
- **Data store:** Google Sheets or Airtable (lightweight, visible, good for a
  live demo)
- **Alerting:** Slack or email node in n8n
- **(Phase 2) Q&A agent:** n8n AI Agent node with a "read rows" tool over the
  same data store

## 7. Success criteria for the demo

- E2E workflow runs live, from triggering a new batch to an alert
  landing in Slack/email, in under a few minutes.
- Risk scores are accompanied by a clear, human-readable explanation — not
  just a number.
- At least one "obviously high risk" and one "obviously low risk" simulated
  batch are included so the range of the system is visible.
- The log/dashboard shows a believable history (multiple batches, multiple
  materials, a visible trend).
- The chat agent correctly answers at least 2–3 sample questions about the logged data and won't answer unrelated questions.

## 8. Risks & open questions

- **Data realism:** Simulated data needs to be believable enough that the
  logic (thresholds, reasoning) looks like it would generalize to real
  company data. Worth basing ideal ranges on real published storage
  guidelines for each material where possible.
- **Threshold tuning:** What risk % should trigger an alert vs. just a log
  entry? Suggest starting at 70%+ = alert, and adjusting based on how the
  demo data plays out.
- **Scope creep:** Phase 2 (chat agent) should only be attempted once Phase 1
  is fully working and demo-ready — it's an enhancement, not a dependency.

## 9. Timeline (suggested)

| Milestone | Target |
|---|---|
| Mock dataset + storage thresholds defined | Day 1–2 |
| Core n8n workflow (trigger → preprocess → AI agent → route) | Day 3–5 |
| Alerting + log/dashboard | Day 6–7 |
| End-to-end testing with varied scenarios | Day 8 |
| (Stretch) Chat Q&A agent | Day 9–10 |
| Demo polish & rehearsal | Day 11–12 |

## 10. Design

- **Colours**: On the dasboard - The main color is red #CF1D1D and the split complementaries are green #1DCF76 and blue #1D76CF. The color white #ffffff may be used for the background and big empty areas.
