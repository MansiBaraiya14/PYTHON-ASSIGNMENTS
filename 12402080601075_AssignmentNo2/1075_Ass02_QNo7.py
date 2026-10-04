import json


def read_records(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                yield None


def transform_records(records):
    for record in records:

        if record is None:
            yield None, None
            continue

        device = record.get("device_id")

        if not device:
            yield None, None
            continue

        try:
            temperature = float(record["temperature_c"])
            humidity = float(record["humidity"])
        except (KeyError, ValueError, TypeError):
            yield device, None
            continue

        # Celsius → Fahrenheit
        temperature_f = temperature * 9 / 5 + 32

        yield device, {
            "temperature_c": temperature,
            "temperature_f": temperature_f,
            "humidity": humidity
        }


def process_records(records):
    summary = {}

    for device, record in records:

        if device is None:
            continue

        if device not in summary:
            summary[device] = {
                "count": 0,
                "min": 0,
                "max": 0,
                "total": 0,
                "corrupted": 0
            }

        data = summary[device]

        # Corrupted record
        if record is None:
            data["corrupted"] += 1
            continue

        temp = record["temperature_c"]

        if data["count"] == 0:
            data["min"] = temp
            data["max"] = temp
        else:
            data["min"] = min(data["min"], temp)
            data["max"] = max(data["max"], temp)

        data["count"] += 1
        data["total"] += temp

    return summary


# Main
file_path = input("Enter JSONL file path: ")

records = read_records(file_path)
transformed = transform_records(records)
summary = process_records(transformed)

for device in sorted(summary):
    data = summary[device]

    if data["count"] > 0:
        average = data["total"] / data["count"]

        print(
            f"{device} count={data['count']} "
            f"min={data['min']:g} "
            f"max={data['max']:g} "
            f"avg={average:.2f} "
            f"corrupted={data['corrupted']}"
        )
    else:
        print(
            f"{device} count=0 "
            f"min=NA max=NA avg=NA "
            f"corrupted={data['corrupted']}"
        )