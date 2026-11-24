#!/usr/bin/env python3
"""Fetch the latest official NY Open Data draw results for Prep."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "lottery-results.json"
BASE = "https://data.ny.gov/resource"
DATASETS = {
    "powerball": "d6yy-54nr",
    "mega_millions": "5xaw-6ayf",
}


def fetch_latest(dataset_id: str) -> dict:
    query = urlencode({"$limit": "1", "$order": "draw_date DESC"})
    url = f"{BASE}/{dataset_id}.json?{query}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "MJR-Prep-Lottery-Feed/1.0 (https://mediajobsreport.com)",
        },
    )
    with urlopen(request, timeout=30) as response:
        rows = json.load(response)

    if not isinstance(rows, list) or not rows:
        raise RuntimeError(f"No rows returned by NY Open Data dataset {dataset_id}")

    row = rows[0]
    draw_date = str(row.get("draw_date", ""))[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", draw_date):
        raise RuntimeError(f"Unexpected draw date in dataset {dataset_id}: {draw_date!r}")

    raw_numbers = re.findall(r"\d+", str(row.get("winning_numbers", "")))
    if dataset_id == DATASETS["powerball"]:
        if len(raw_numbers) < 6:
            raise RuntimeError(f"Expected five Powerball numbers and a Powerball; got {raw_numbers!r}")
        numbers, special = [int(value) for value in raw_numbers[:5]], int(raw_numbers[5])
        multiplier = row.get("multiplier")
    else:
        if len(raw_numbers) < 5:
            raise RuntimeError(f"Expected five Mega Millions numbers; got {raw_numbers!r}")
        numbers = [int(value) for value in raw_numbers[:5]]
        special_raw = re.findall(r"\d+", str(row.get("mega_ball", "")))
        if not special_raw:
            raise RuntimeError("Mega Millions row did not include mega_ball")
        special = int(special_raw[0])
        multiplier = row.get("multiplier")

    multiplier_text = str(multiplier).strip() if multiplier is not None else ""
    if multiplier_text and multiplier_text.lower().endswith(("x", "×")):
        multiplier_text = multiplier_text[:-1].strip()
    if multiplier_text:
        multiplier_text += "×"
    else:
        multiplier_text = "Not posted"

    return {
        "draw_date": draw_date,
        "numbers": numbers,
        "special": special,
        "multiplier": multiplier_text,
    }


def main() -> None:
    payload = {
        "source": "New York State Gaming Commission via NY Open Data",
        "datasets": DATASETS,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "games": {
            "powerball": fetch_latest(DATASETS["powerball"]),
            "mega_millions": fetch_latest(DATASETS["mega_millions"]),
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        old = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if old.get("games") == payload["games"]:
            print("NY Open Data has no new lottery results; feed unchanged.")
            return

    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT.relative_to(ROOT)} with the latest draw results.")


if __name__ == "__main__":
    main()
