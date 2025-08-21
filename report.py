# report.py
import json, os
from collections import Counter
from datetime import datetime


def generate_moods_report(data_file="moods.json", output_dir=".", now=None):
    moods = []
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            try:
                moods = json.load(f)
                if not isinstance(moods, list):
                    moods = []
            except json.JSONDecodeError:
                moods = []

    total = len(moods)

    counter = {}
    for m in moods:
        m = m.strip()
        if m in counter:
            counter[m] += 1
        else:
            counter[m] = 1

    distribution = {}
    for m, c in counter.items():
        dist = (c / total) * 100
        distribution[m] = f"{dist:.2f}%"

    ts = now or datetime.now().replace(microsecond=0).isoformat()
    out_path = os.path.join(output_dir, f"moods-report-{ts}.json")

    try:
        f = open(out_path, "w")
        json.dump(distribution, f, indent=2)
    finally:
        f.close()

    with open(out_path, "w") as f:
        json.dump(distribution, f, indent=2)

    return distribution, out_path
