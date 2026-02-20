from reports.reporting import AverageGDPReport


def test_average_gdp_report_aggregates_across_records_and_sorts_desc() -> None:
    records = [
        {"country": "United States", "gdp": "25462"},
        {"country": "United States", "gdp": "23315"},
        {"country": "China", "gdp": "17963"},
        {"country": "China", "gdp": "17734"},
        {"country": "Germany", "gdp": "4086"},
        {"country": "Germany", "gdp": "4072"},
    ]

    rows = AverageGDPReport().generate(records)

    assert rows == [
        ["United States", 24388.5],
        ["China", 17848.5],
        ["Germany", 4079.0],
    ]
