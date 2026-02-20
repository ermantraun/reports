from pathlib import Path

from reports.cli import run


def test_run_prints_average_gdp_report_for_multiple_files(capsys, tmp_path: Path) -> None:
    file1 = tmp_path / "data_1.csv"
    file1.write_text(
        "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
        "United States,2023,25462,2.1,3.4,3.7,339,North America\n"
        "China,2023,17963,5.2,2.5,5.2,1425,Asia\n",
        encoding="utf-8",
    )

    file2 = tmp_path / "data_2.csv"
    file2.write_text(
        "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
        "United States,2022,23315,2.1,8.0,3.6,338,North America\n"
        "China,2022,17734,3.0,2.0,5.6,1423,Asia\n"
        "Germany,2022,4072,1.8,8.7,3.1,83,Europe\n",
        encoding="utf-8",
    )

    exit_code = run(["--files", str(file1), str(file2), "--report", "average-gdp"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "| country" in captured.out
    assert "United States" in captured.out
    assert "24388.5" in captured.out
    assert "China" in captured.out
    assert "17848.5" in captured.out
    assert "Germany" in captured.out


def test_run_returns_error_for_unknown_report(capsys, tmp_path: Path) -> None:
    file1 = tmp_path / "data.csv"
    file1.write_text(
        "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
        "United States,2023,25462,2.1,3.4,3.7,339,North America\n",
        encoding="utf-8",
    )

    exit_code = run(["--files", str(file1), "--report", "unknown-report"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Неизвестный отчёт" in captured.err


def test_run_returns_error_for_missing_files(capsys) -> None:
    exit_code = run(["--files", "not_found.csv", "--report", "average-gdp"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Файлы не найдены" in captured.err
