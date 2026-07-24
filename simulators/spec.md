# Batch Simulator Specification

**Purpose:**  
The `batch_simulator.py` module generates simulated batch data representing raw material lots for the Spoilage Quality Risk Alert System. It provides deterministic yet flexible mechanisms to produce realistic batch instances with controlled deviations from ideal storage conditions.

---  

## Table of Contents
1. [Overview](#overview)  
2. [Dependencies](#dependencies)  
3. [Core Functions](#core-functions)  
   - [`generate_batch`](#generate_batch)  
   - [`_validate_input_params`](#_validate_input_params)  
4. [Configuration Parameters](#configuration-parameters)  
5. [Testing Strategy](#testing-strategy)  
6. [Example Usage](#example-usage)  
7. [Extensibility](#extensibility)  

---  

## Overview
`batch_simulator.py` is responsible for synthesizing batch records used by the preprocessing stage (`processor/pre-processor.py`). Each batch contains:
- Unique identifier and generation timestamp
- Container-level temperature and humidity values
- List of materials with their storage duration
- Synthetic metadata used for downstream AI risk evaluation

The simulator supports configurable ranges for key parameters to allow targeted testing of edge cases and normal operating conditions.

---  

## Dependencies
The module relies on standard Python libraries only:
- `datetime` – for generating realistic timestamps
- `uuid` – for creating UUID-based batch IDs
- `random` – for stochastic value generation within defined ranges
- `typing` – for type hints and validation helpers

No external data sources are required, enabling offline operation.

---  

## Core Functions

### `generate_batch`

```python
def generate_batch(
    *,
    seed: int | None = None,
    material_count: int = 5,
    batch_id: str | None = None,
    base_timestamp: str | None = None,
    min_temp: int = 5,
    max_temp: int = 35,
    min_humidity: int = 10,
    max_humidity: int = 95,
    min_storage_days: int = 1,
    max_storage_days: int = 1825,
    probability_of_out_of_spec: float = 0.3,
) -> dict:
    """
    Generate a deterministic batch of synthetic material lots.

    Parameters:
        seed: Optional integer seed for reproducible results.
        material_count: Number of distinct materials in the batch.
        batch_id: Optional identifier; if omitted, a UUID will be generated.
        base_timestamp: Optional ISO 8601 timestamp to anchor batch generation.
        min_/max_temp/humidity: Range limits for generated environmental readings.
        min_/max_storage_days: Storage duration limits for generated materials.
        probability_of_out_of_spec: Chance that a material will exceed storage limits.

    Returns:
        dict: A dictionary matching the expected JSON schema for simulation input.
    """
```

**Key Behaviors:**
- Initializes a random seed if provided for reproducibility.
- Randomly selects temperature, humidity, and storage days within configured ranges.
- Applies `probability_of_out_of_spec` to ensure some materials violate limits.
- Returns a dictionary containing `batch_id`, `timestamp`, and `materials` list.

### `_validate_input_params`

```python
def _validate_input_params(
    material_count: int,
    min_temp: int,
    max_temp: int,
    min_humidity: int,
    max_humidity: int,
    min_storage_days: int,
    max_storage_days: int,
    probability_of_out_of_spec: float,
) -> None:
    """
    Validate that numeric inputs are within plausible ranges.
    Raises:
        ValueError: If any parameter violates constraints.
    """
```

**Validation Rules:**
- `material_count` must be ≥ 1
- `min_temp` < `max_temp`
- `min_humidity` < `max_humidity`
- `min_storage_days` < `max_storage_days`
- `0` ≤ `probability_of_out_of_spec` ≤ 1

---  

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|------------|
| `material_count` | `5` | Number of distinct material entries per batch. Adjust for workload intensity. |
| `min_temp` / `max_temp` | `5` / `35` | Temperature range in Celsius for container environment. |
| `min_humidity` / `max_humidity` | `10` / `95` | Humidity range in percent relative humidity. |
| `min_storage_days` / `max_storage_days` | `1` / `1825` (5 years) | Storage duration limits for generated materials. |
| `probability_of_out_of_spec` | `0.3` | Target proportion of materials that should exceed permit thresholds. |
| `seed` | `None` | Seed for deterministic simulation; omitting yields nondeterministic output. |

---  

## Testing Strategy

1. **Unit Tests**
   - Verify that `_validate_input_params` raises `ValueError` on invalid inputs.
   - Confirm reproducibility when a fixed `seed` is supplied.
   - Ensure returned keys (`batch_id`, `timestamp`, `materials`) always exist.

2. **Integration Tests**
   - Feed simulator output into `processor/pre-processor.py` and confirm:
     - No exceptions during preprocessing.
     - Expected deviation calculations occur.
   - Validate that some materials are flagged as out‑of‑spec when `probability_of_out_of_spec` > 0.

3. **Edge‑Case Scenarios**
   - Test batches with a single material or many materials.
   - Stress test with extreme temperature/humidity ranges.
   - Validate behavior when `storage_max_days` is `None` (unlimited shelf life).

---  

## Example Usage

```python
from batch_simulator import generate_batch

# Create a batch with a fixed seed for repeatable results
batch = generate_batch(
    seed=42,
    material_count=3,
    probability_of_out_of_spec=0.5,
    base_timestamp="2026-07-23T12:00:00Z"
)

print(batch)
```

**Sample Output:**
```json
{
  "batch_id": "d3f1e2a8-5c9b-4e7f-9b2a-1c2e4f5b6a7c",
  "timestamp": "2026-07-23T12:00:00Z",
  "materials": [
    {
      "name": "flour",
      "storage_days": 120,
      "out_of_spec": false
    },
    {
      "name": "yeast",
      "storage_days": 800,
      "out_of_spec": true
    },
    {
      "name": "dairy_powder",
      "storage_days": 1500,
      "out_of_spec": false
    }
  ],
  "containers": {
    "temperature": 23,
    "humidity": 67
  }
}
```

---  

## Extensibility

Future enhancements may include:
- Supporting multiple storage units with distinct environmental profiles.
- Adding material‑specific constraint profiles (e.g., preferred temperature zones).
- Exporting batch data to external schemas such as JSON Lines or CSV.
- Integrating with realistic weather feed data for dynamic condition simulation.

This design ensures the simulator remains lightweight while offering sufficient flexibility for thorough risk evaluation testing.  

</details>

---  

*Document generated on 2026-07-23 by the Spoilage Quality Risk Alert System development team.*