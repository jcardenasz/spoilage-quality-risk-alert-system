# Plan: Batch Data Simulation Module

## Context
The user is a student building a Proof of Concept (POC) for a Raw Material Quality & Spoilage Risk Alert System. The system needs realistic simulated batch data that can later be fed into n8n for AI risk evaluation. Phase 1 is focused on creating the data generation module.

## Requirements (from PRD)
- Each batch = 100kg container holding five 20kg boxes (flour, sugar, yeast, dairy powder, cocoa)
- Per-batch storage conditions (shared container): temperature (°C), relative humidity (%)
- Per-material storage time (days) - each material has different optimal ranges
- Ideal ranges from PRD section 2.1:
  - Flour: 10-20°C, <80% humidity, 365 days max
  - Sugar: 15-25°C, <65% humidity, no expiry
  - Yeast: 15-25°C, <60% humidity, 730 days max (2 years)
  - Dairy Powder: 15-20°C, <60% humidity, 730 days max
  - Cocoa: 15-20°C, <50% humidity, 1095 days max (3 years)
- Output: realistic data with occasional "risk-inducing" edge cases
- Include: temperature: int, humidity: int, time_stored: int, risk: int (placeholder), risk_statement: text (placeholder), timestamp: date

## Recommended Approach

### Language Choice: Python
**Why Python?**
1. Better statistical libraries (random + numpy distributions)
2. Easy to read and understand for a student learning
3. JSON output can be easily imported into n8n
4. Can run standalone to test before integration

### File Structure
- `simulators/batch_simulator.py` - Main generator script

### Implementation Logic

```python
# For each batch (default: 10 batches per run):
# 1. Generate timestamp (current date in 2026-07-21 range)
# 2. Generate container temperature (shared acros all materials):
#    - Normal range: 12-28°C (center of most ideal ranges)
#    - 20% chance: temperature spike (30-40°C) - causes high risk
# 3. Generate container humidity (shared):
#    - Normal range: 30-70%
#    - 20% chance: high humidity (75-95%) - triggers risk
# 4. For each material, generate storage days:
#    - Within 5% of ideal = low risk
#    - Near/over max = high risk
# 5. Occasionally combine multiple risk factors (20% chance per batch)
# 6. Output to JSON with placeholder risk fields
```

### Educational Comments
- Each function and logic block will explain WHY certain ranges were chosen
- Include PRD references as comments
- Show how values map to risk categories (Risk 1: 0-34%, Risk 2: 35-69%, Risk 3: 70-100%)

## Critical Files to Create
1. `/mnt/d/Proyectos personales/spoilage-quality-risk-alert-system/simulators/batch_simulator.py`

## Verification
1. Run the script: `python simulators/batch_simulator.py`
2. Check that output JSON contains realistic values
3. Verify at least one high-risk and one low-risk batch in 10-run output
4. Confirm all 6 required fields present per batch

## Questions for User (via AskUserQuestion)
- How many batches should be generated per run?
- Any preference for Python vs JavaScript?