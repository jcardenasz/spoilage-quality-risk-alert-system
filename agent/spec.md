# AI Agent Specification for Spoilage Quality Risk Evaluation

**Purpose:**  
Develop a comprehensive specification document for the AI agent responsible for evaluating spoilage risks based on batch deviation data. This specification ensures consistency in output format and aligns with system requirements.

---

## Table of Contents
1. [Overview](#overview)  
2. [Core Functionality](#core-functionality)  
3. [Input Data Schema](#input-data-schema)  
4. [Risk Categorization Logic](#risk-categorization)  
5. [Output Format Requirements](#output-format-requirements)  
6. [Implementation Constraints](#implementation-constraints)  
7. [Testing Strategy](#testing-strategy)  

---

## Overview
Evaluates batch-level storage deviation data to assign one of three risk categories (1-3) and generates compliance-focused risk statements. Processes data from n8n workflows and interfaces with alert systems. The agent receives pre-computed deviation data from the pre-processor and outputs a risk assessment in a strict JSON Array format.

---

## Core Functionality

- **Validation:** Ensures input conforms to expected schema before processing
- **Risk Scoring:** Calculates composite risk scores based on multi-factor deviation data
- **Classification:** Assigns one of three risk categories using threshold logic
- **Statement Generation:** Creates human-readable explanations suitable for warehouse administrators
- **Consistency:** Applies identical logic across all batches in a workflow execution

---

## Input Data Schema

The agent receives pre-processed batches with the following structure:

```json
{
  "batch_id": 42,
  "container": {
    "temperature": 22.5,
    "humidity": 75.0,
    "materials_out_of_spec": 1,
    "total_deviation": 12.5
  },
  "materials": [
    {
      "name": "flour",
      "storage_days_deviation": 0,
      "temperature_deviation": 2,
      "humidity_deviation": 0
    }
  ]
}
```

### Input Fields

| Field | Type | Description |
|-------|------|-------------|
| `batch_id` | integer | Unique batch identifier (preserve exact type) |
| `container.temperature` | float | Current storage temperature |
| `container.humidity` | float | Current relative humidity |
| `container.materials_out_of_spec` | integer | Count of non-compliant materials |
| `container.total_deviation` | float | Sum of all deviations across materials |
| `materials[].name` | string | Material identifier |
| `materials[].temperature_deviation` | float | Deviation from ideal range |
| `materials[].humidity_deviation` | float | Amount above humidity maximum |
| `materials[].storage_days_deviation` | float | Days past maximum storage limit |

---

## Risk Categorization Logic

### Category 1 - Minimum (risk_number: 1)
- All deviation values are zero or negligible
- All materials are within their acceptable storage ranges
- No alert is triggered

### Category 2 - Medium (risk_number: 2)
- One or more materials show moderate deviations
- Single-factor breaches with manageable magnitude
- Batch inspection and verification of storage conditions recommended
- Triggers an automatic email alert to the administrator

### Category 3 - High (risk_number: 3)
- Significant deviations across multiple materials or factors
- One or more materials breach multiple thresholds simultaneously
- High likelihood of quality degradation or spoilage
- Immediate inspection required before batch release
- Triggers an automatic email alert to the administrator

### Evaluation Rules
1. Evaluate combined severity across all materials in the batch
2. Larger deviations contribute proportionally more risk
3. Multi-factor breaches from a single material are weighted more heavily
4. Temperature and humidity deviations are considered equally important
5. Batch age compounds risk when storage_days_deviation is present

---

## Output Format Requirements

The agent must output **ONLY** a valid JSON array with no markdown, no code fences, and no commentary.

### Output Schema

```json
[
  {
    "batch_id": "<same integer from the input batch, exactly copied>",
    "risk_number": <1, 2, or 3>,
    "risk_statement": "<natural language explanation>"
  }
]
```

### risk_statement Guidelines

- Name specific materials and factors driving the risk with exact numbers from the input
- State how far over a threshold a given factor is, with the material name
- Include batch age context when storage_days_deviation is present and non-zero
- Use formal, compliance-focused language suitable for warehouse administrators
- Keep to 2-4 sentences
- For category 2 or 3, explicitly state that an alert has been issued
- For category 1, state that no alert is required and recommend continued routine monitoring

### Output Constraints

- No markdown formatting (no code fences, no bold, no headers)
- No commentary or preamble text
- No percentages (risk_number must be integer 1, 2, or 3)
- No reformatting or type conversion of batch_id (preserve integer type exactly)
- One output object per input batch

---

## Implementation Constraints

1. **Never invent** thresholds, materials, or numerical values not present in the input
2. **Never adjust** or override input data values
3. **Never recommend** storage modifications or process changes outside quality inspection
4. **Never use** speculative or hedging language (e.g., "might", "possibly")
5. **Never fabricate** a batch_id — always use the one from the input exactly as provided
6. **Never mix** batch_ids between batches — each output batch_id must match its own input batch

---

## Testing Strategy

### Unit Tests
- Verify category 1 assigned when all deviations are zero
- Verify category 3 assigned when multiple materials breach multiple thresholds
- Verify output is valid JSON array with correct schema
- Verify batch_id type is preserved as integer in output

### Integration Tests
- Feed pre-processor output to agent and confirm output structure
- Test boundary between categories 1 and 2
- Verify alert triggering logic matches risk category

### Edge Cases
- Single material batches with extreme deviations
- Batches where all materials are simultaneously out of spec
- Batches with storage_days_deviation but zero temperature/humidity deviations

---

*Document generated on 2026-07-23 by the Spoilage Quality Risk Alert System development team.*
