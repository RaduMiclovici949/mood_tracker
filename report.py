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
    counts = Counter([str(m).strip() for m in moods if str(m).strip()])
    distribution = {m: f"{(c/total)*100:.2f}%" for m, c in counts.items()} if total else {}

    ts = (now or datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))
    out_path = os.path.join(output_dir, f"moods-report-{ts}.json")
    with open(out_path, "w") as f:
        json.dump(distribution, f, indent=2)

    return distribution, out_path

