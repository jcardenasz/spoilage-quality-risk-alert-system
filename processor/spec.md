# Pre-Processor Specification

**Purpose:**  
The `pre-processor.py` module validates incoming batch data against material-specific storage parameters and computes risk metrics prior to AI-based risk evaluation in the Spoilage Quality Risk Alert System.

---

## Table of Contents
1. [Overview](#overview)  
2. [Dependencies](#dependencies)  
3. [Core Functions](#core-functions)  
   - [`calculate_temperature_deviation`](#calculate_temperature_deviation)  
   - [`calculate_humidity_deviation`](#calculate_humidity_deviation)  
   - [`calculate_storage_deviation`](#calculate_storage_deviation)  
   - [`process_batch`](#process_batch)  
4. [Configuration Parameters](#configuration-parameters)  
5. [Testing Strategy](#testing-strategy)  
6. [Example Usage](#example-usage)  
7. [Extensibility](#extensibility)  

---

## Overview
`pre-processor.py` acts as the data validation layer for the spoilage risk pipeline. It receives a batch record (typically produced by `simulators/batch_simulator.py`), evaluates each material's storage conditions against predefined limits, and produces a structured output containing deviation metrics. These metrics are then consumed by the AI risk agent to determine alert levels.

The module is designed to run within an n8n **Function** node, where it processes a single batch per invocation and returns a JSON-compatible dictionary.

---

## Dependencies
The module uses only standard Python features:
- `typing` – for type hints and schema documentation
- `json` – for serialization compatibility (optional, when used outside n8n)

No external packages or network calls are required, ensuring lightweight and portable execution.

---

## Core Functions

### `calculate_temperature_deviation`

```python
def calculate_temperature_deviation(actual: float, minimum: float, maximum: float) -> float:
    """
    Compute how far the actual temperature deviates from the acceptable range.

    Parameters:
        actual: Measured container temperature.
        minimum: Lower bound of acceptable temperature.
        maximum: Upper bound of acceptable temperature.

    Returns:
        float: Negative value if below minimum, positive if above maximum, 0 if within range.
    """
```

**Key Behaviors:**
- Returns a negative value if `actual` is below `minimum`.
- Returns a positive value if `actual` is above `maximum`.
- Returns `0` if the temperature is within the acceptable range.

---

### `calculate_humidity_deviation`

```python
def calculate_humidity_deviation(actual: float, maximum: float) -> float:
    """
    Compute how far the actual humidity exceeds the maximum allowed value.

    Parameters:
        actual: Measured relative humidity.
        maximum: Maximum acceptable humidity level.

    Returns:
        float: Positive deviation if humidity exceeds maximum, otherwise 0.
    """
```

**Key Behaviors:**
- Only an upper bound is considered (no lower bound for humidity).
- Returns `0` if humidity is at or below the maximum.

---

### `calculate_storage_deviation`

```python
def calculate_storage_deviation(actual: int, maximum: int | None) -> int:
    """
    Compute how far the actual storage duration exceeds the maximum allowed days.

    Parameters:
        actual: Number of days the material has been stored.
        maximum: Maximum allowed storage days (None indicates no expiration).

    Returns:
        int: Positive deviation if storage exceeds maximum, otherwise 0.
    """
```

**Key Behaviors:**
- Returns `0` if `maximum` is `None` (unlimited shelf life).
- Returns `0` if `actual` is within the allowed range.
- Returns a positive deviation if storage duration exceeds the limit.

---

### `process_batch`

```python
def process_batch(batch: dict) -> dict:
    """
    Validate a single batch against material limits and compute risk metrics.

    Parameters:
        batch: Dictionary containing batch_id, timestamp, temperature, humidity, and materials list.

    Returns:
        dict: Structured dictionary with processed materials and aggregated risk indicators.
    """
```

**Key Behaviors:**
- Iterates over each material in the batch.
- Looks up acceptable limits from `MATERIAL_LIMITS`.
- Calculates temperature, humidity, and storage deviations for each material.
- Tracks total deviation and count of out-of-spec materials.
- Returns a structured dictionary containing:
  - `batch_id` and `timestamp` (passed through from input)
  - `container` summary with total deviation and out-of-spec count
  - `materials` list with per-material deviation details

---

## Configuration Parameters

| Parameter | Description | Example Value |
|-----------|-------------|---------------|
| `MATERIAL_LIMITS` | Dictionary mapping material names to their acceptable storage parameters. | See below |
| `temperature.min` / `temperature.max` | Acceptable temperature range in Celsius for a given material. | `10` / `20` for flour |
| `humidity_max` | Maximum acceptable relative humidity percentage. | `80` for flour |
| `storage_max_days` | Maximum allowed storage duration in days (`None` = unlimited). | `365` for flour |

**Example `MATERIAL_LIMITS` definition:**
```python
MATERIAL_LIMITS = {
    "flour": {
        "temperature": {"min": 10, "max": 20},
        "humidity_max": 80,
        "storage_max_days": 365
    },
    "sugar": {
        "temperature": {"min": 15, "max": 25},
        "humidity_max": 65,
        "storage_max_days": None
    },
    "yeast": {
        "temperature": {"min": 15, "max": 25},
        "humidity_max": 60,
        "storage_max_days": 730
    },
    # Additional materials as needed...
}
```

---

## Testing Strategy

1. **Unit Tests**
   - Verify deviation calculations return correct values for in-range, below-minimum, and above-maximum inputs.
   - Confirm `calculate_storage_deviation` handles `None` maximum correctly.
   - Validate that `process_batch` correctly counts out-of-spec materials.

2. **Integration Tests**
   - Feed simulated batches (from `simulators/batch_simulator.py`) into `process_batch`.
   - Confirm output structure matches the expected schema.
   - Validate that `total_deviation` reflects the sum of all individual deviations.

3. **Edge-Case Scenarios**
   - Test batches with zero materials.
   - Test with materials not present in `MATERIAL_LIMITS` (should raise `KeyError`).
   - Test with extreme temperature/humidity values.
   - Test with `storage_max_days` set to `None`.

---

## Example Usage

```python
from pre_processor import process_batch

batch = {
    "batch_id": "BATCH-001",
    "timestamp": "2026-07-23T12:00:00Z",
    "temperature": 22,
    "humidity": 75,
    "materials": [
        {"name": "flour", "storage_days": 100},
        {"name": "yeast", "storage_days": 800}
    ]
}

result = process_batch(batch)
print(result)
```

**Sample Output:**
```json
{
  "batch_id": "BATCH-001",
  "timestamp": "2026-07-23T12:00:00Z",
  "container": {
    "temperature": 22,
    "humidity": 75,
    "materials_out_of_spec": 1,
    "total_deviation": 72.0
  },
  "materials": [
    {
      "name": "flour",
      "storage_days": 100,
      "expected_storage_days": 365,
      "storage_days_deviation": 0,
      "expected_temperature": {"min": 10, "max": 20},
      "temperature_deviation": 2,
      "humidity": 75,
      "expected_humidity_max": 80,
      "humidity_deviation": 0
    },
    {
      "name": "yeast",
      "storage_days": 800,
      "expected_storage_days": 730,
      "storage_days_deviation": 70,
      "expected_temperature": {"min": 15, "max": 25},
      "temperature_deviation": 0,
      "humidity": 75,
      "expected_humidity_max": 60,
      "humidity_deviation": 15
    }
  ]
}
```

---

## Extensibility

Future enhancements may include:
- Adding warning thresholds (e.g., 10% deviation = yellow alert).
- Supporting batch similarity detection for anomaly correlation.
- Implementing expiration date calculations based on the current date.
- Adding support for custom material constraint profiles.
- Integrating with real-time sensor data feeds for live validation.

This design ensures the preprocessor remains lightweight while providing a robust foundation for risk-based alerting.

---

*Document generated on 2026-07-23 by the Spoilage Quality Risk Alert System development team.*