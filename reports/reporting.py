from __future__ import annotations

from collections import defaultdict
from typing import Any, Protocol


class Report(Protocol):
    name: str

    def generate(self, records: list[dict[str, str]]) -> list[list[Any]]:
        ...


class AverageGDPReport:
    name = "average-gdp"

    def generate(self, records: list[dict[str, str]]) -> list[list[Any]]:
        gdp_values_by_country: dict[str, list[float]] = defaultdict(list)

        for record in records:
            country = record["country"]
            gdp = float(record["gdp"])
            gdp_values_by_country[country].append(gdp)

        rows: list[list[Any]] = []
        for country, gdp_values in gdp_values_by_country.items():
            avg_gdp = sum(gdp_values) / len(gdp_values)
            rows.append([country, round(avg_gdp, 2)])

        rows.sort(key=lambda row: row[1], reverse=True)
        return rows


REPORT_REGISTRY: dict[str, Report] = {
    AverageGDPReport.name: AverageGDPReport(),
}


def get_report(report_name: str) -> Report | None:
    return REPORT_REGISTRY.get(report_name)
