"""
batch_simulator.py
==================

Generates realistic simulated batch data for the Raw Material Quality &
Spoilage Risk Alert System POC.

Each batch is a 100 kg hygienic container holding five 20 kg boxes:
    flour, sugar, yeast, dairy powder, cocoa

For every batch we record the *shared* container conditions (temperature,
humidity) and the *per-material* storage time.  A small percentage of
batches intentionally drift into "risk-inducing" territory so that the
downstream AI risk agent has something interesting to evaluate.

Run:
    python3 simulators/batch_simulator.py            # 5 batches (default)
    python3 simulators/batch_simulator.py --count 10 # custom count

Output:
    JSON lines written to stdout and saved to
    data/generated_batches.json
"""

import json
import os
import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# 1.  Material reference table  (PRD §2.1 "Materials Optimal Factors")
# ---------------------------------------------------------------------------
# Each material has an ideal temperature range, a maximum relative humidity,
# and a maximum recommended storage time in days.
#
# Sugar has "NO EXP" in the PRD — but per user request we now cap its storage
# at 3 years (≈1 095 days) to keep numbers realistic.
MATERIALS = {
    "flour": {
        "temp_min": 10,
        "temp_max": 20,
        "humidity_max": 80,
        "max_storage_days": 365
    },
    "sugar": {
        "temp_min": 15,
        "temp_max": 25,
        "humidity_max": 65,
        "max_storage_days": None,          # No expiration (PRD)
        "simulation_max_days": 1825        # Generate up to 5 years
    },
    "yeast": {
        "temp_min": 15,
        "temp_max": 25,
        "humidity_max": 60,
        "max_storage_days": 730
    },
    "dairy_powder": {
        "temp_min": 15,
        "temp_max": 20,
        "humidity_max": 60,
        "max_storage_days": 730
    },
    "cocoa": {
        "temp_min": 15,
        "temp_max": 20,
        "humidity_max": 50,
        "max_storage_days": 1095
    },
}


# ---------------------------------------------------------------------------
# 2.  Helper functions
# ---------------------------------------------------------------------------
def generate_container_conditions(risk_inducing=False):
    """
    Generate the *shared* storage conditions for a batch container.

    Parameters
    ----------
    risk_inducing : bool
        When True the values are deliberately pushed toward the edges of
        acceptable ranges so the AI agent will flag them.

    Returns
    -------
    (temperature: int, humidity: int)
    """
    if risk_inducing:
        # Temperature spike: 30–40 °C (well above any ideal range)
        temperature = random.randint(30, 40)
        # Humidity spike: 75–95 % (above most material limits)
        humidity = random.randint(75, 95)
    else:
        # Normal operating band: 12–28 °C covers the overlap of all
        # material ideal ranges while leaving room for variation.
        temperature = random.randint(12, 28)
        # Normal humidity: 30–70 % (below all material limits)
        humidity = random.randint(30, 70)

    return temperature, humidity


def generate_storage_days(material_name, risk_inducing=False):
    # Generate a realistic storage time (days) for one material.

    limits = MATERIALS[material_name]

    # Sugar has no expiration.
    if limits["max_storage_days"] is None:

        simulation_max = limits["simulation_max_days"]

        if risk_inducing:
            return random.randint(
                int(simulation_max * 0.60),
                simulation_max
            )

        return random.randint(
            30,
            int(simulation_max * 0.50)
        )

    max_days = limits["max_storage_days"]

    if risk_inducing:
        low = int(max_days * 0.70)
        high = int(max_days * 1.10)
        return random.randint(low, high)

    low = max(1, int(max_days * 0.05))
    high = int(max_days * 0.60)

    return random.randint(low, high)

def generate_timestamp():
    """
    Return a timestamp string for *today* (the POC runs in July 2026).
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# 3.  Batch generator
# ---------------------------------------------------------------------------
def generate_batch(batch_id, risk_inducing=False):
    """
    Build a single batch dictionary.

    Fields
    ------
    batch_id          : str   — unique identifier
    temperature         : int   — container temperature (°C)
    humidity            : int   — container relative humidity (%)
    materials           : dict  — per-material storage_days
    risk_number         : int   — placeholder (filled by AI agent later)
    risk_statement      : str   — placeholder (filled by AI agent later)
    timestamp           : str   — ISO-8601 timestamp
    """
    temperature, humidity = generate_container_conditions(risk_inducing)

    materials = []
    for mat_name in MATERIALS:
        materials.append({
        "name": mat_name,
        "storage_days": generate_storage_days(
            mat_name,
            risk_inducing
        )
    })

    return {
        "batch_id": batch_id,
        "temperature": temperature,
        "humidity": humidity,
        "materials": materials,
        "risk_number": 0,          # placeholder — AI agent fills this
        "risk_statement": "",     # placeholder — AI agent fills this
        "timestamp": generate_timestamp(),
    }


# ---------------------------------------------------------------------------
# 4.  Main entry point
# ---------------------------------------------------------------------------
def main(count=5):
    """
    Generate *count* batches and print/save them as JSON.

    ~20 % of batches are marked risk_inducing so the output always
    contains at least one high-risk candidate for the AI agent to
    evaluate.
    """
    batches = []
    for i in range(count):
        batch_id = f"BATCH-{datetime.now().strftime('%Y%m%d')}-{i+1:03d}"
        # ~20 % chance of a risk-inducing batch
        risk_inducing = random.random() < 0.20
        batch = generate_batch(batch_id, risk_inducing)
        batches.append(batch)

    # Pretty-print to stdout for quick inspection
    print(json.dumps(batches, indent=2))

    # Persist to disk so n8n (or any consumer) can pick it up
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "generated_batches.json")
    with open(output_path, "w") as f:
        json.dump(batches, f, indent=2)
    print(f"\nSaved {len(batches)} batches to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate simulated batch data for the Spoilage Risk POC"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=5,
        help="Number of batches to generate (default: 5)",
    )
    args = parser.parse_args()
    main(count=args.count)