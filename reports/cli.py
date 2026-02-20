from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tabulate import tabulate

from reports.data_loader import load_records
from reports.reporting import REPORT_REGISTRY, get_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Формирование отчётов по макроэкономическим CSV данным.")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV файлам с данными.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help=f"Название отчёта. Доступно: {', '.join(REPORT_REGISTRY.keys())}",
    )
    return parser


def validate_args(files: list[str], report_name: str) -> list[str]:
    errors: list[str] = []

    missing_files = [file_path for file_path in files if not Path(file_path).exists()]
    if missing_files:
        errors.append(f"Файлы не найдены: {', '.join(missing_files)}")

    if report_name not in REPORT_REGISTRY:
        available = ", ".join(sorted(REPORT_REGISTRY.keys()))
        errors.append(f"Неизвестный отчёт '{report_name}'. Доступные отчёты: {available}")

    return errors


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    errors = validate_args(args.files, args.report)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 2

    records = load_records(args.files)
    report = get_report(args.report)
    if report is None:
        print(f"Неизвестный отчёт '{args.report}'", file=sys.stderr)
        return 2

    rows = report.generate(records)
    print(tabulate(rows, headers=["country", "average_gdp"], tablefmt="github"))
    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
