MATERIAL_LIMITS = {
    "flour": {"temperature": {"min": 10, "max": 20}, "humidity_max": 80, "storage_max_days": 365},
    "sugar": {"temperature": {"min": 15, "max": 25}, "humidity_max": 65, "storage_max_days": None},
    "yeast": {"temperature": {"min": 15, "max": 25}, "humidity_max": 60, "storage_max_days": 730},
    "dairy_powder": {"temperature": {"min": 15, "max": 20}, "humidity_max": 60, "storage_max_days": 730},
    "cocoa": {"temperature": {"min": 15, "max": 20}, "humidity_max": 50, "storage_max_days": 1095},
}


def calculate_temperature_deviation(actual, minimum, maximum):
    if actual < minimum:
        return actual - minimum
    if actual > maximum:
        return actual - maximum
    return 0


def calculate_humidity_deviation(actual, maximum):
    if actual > maximum:
        return actual - maximum
    return 0


def calculate_storage_deviation(actual, maximum):
    if maximum is None:
        return 0
    if actual > maximum:
        return actual - maximum
    return 0


def process_batch(batch):
    processed_materials = []
    materials_out_of_spec = 0
    total_deviation = 0

    for material in batch["materials"]:
        name = material["name"]
        limits = MATERIAL_LIMITS[name]

        temperature_dev = calculate_temperature_deviation(
            batch["temperature"], limits["temperature"]["min"], limits["temperature"]["max"]
        )
        humidity_dev = calculate_humidity_deviation(batch["humidity"], limits["humidity_max"])
        storage_dev = calculate_storage_deviation(material["storage_days"], limits["storage_max_days"])

        material_has_issue = temperature_dev != 0 or humidity_dev != 0 or storage_dev != 0
        if material_has_issue:
            materials_out_of_spec += 1

        total_deviation += abs(temperature_dev)
        total_deviation += humidity_dev
        total_deviation += storage_dev

        processed_materials.append({
            "name": name,
            "storage_days": material["storage_days"],
            "expected_storage_days": limits["storage_max_days"] if limits["storage_max_days"] else "NO_EXPIRATION",
            "storage_days_deviation": storage_dev,
            "expected_temperature": {"min": limits["temperature"]["min"], "max": limits["temperature"]["max"]},
            "temperature_deviation": temperature_dev,
            "humidity": batch["humidity"],
            "expected_humidity_max": limits["humidity_max"],
            "humidity_deviation": humidity_dev,
        })

    return {
        "batch_id": batch["batch_id"],
        "timestamp": batch["timestamp"],
        "container": {
            "temperature": batch["temperature"],
            "humidity": batch["humidity"],
            "materials_out_of_spec": materials_out_of_spec,
            "total_deviation": total_deviation,
        },
        "materials": processed_materials,
    }


# --- n8n entry point (replaces the __main__ block) ---
results = []

batch = _item["json"]
return {"json": process_batch(batch)}