from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


Record = dict[str, str]


def load_records(file_paths: Iterable[str]) -> list[Record]:
    records: list[Record] = []

    for file_path in file_paths:
        path = Path(file_path)
        with path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            records.extend(reader)

    return records
