# CSV Macro Reports

Небольшой CLI-скрипт для построения отчётов по CSV-файлам с макроэкономическими данными.
Сейчас реализован отчёт `average-gdp`: средний ВВП по странам по всем переданным файлам.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python -m reports.cli --files examples/data_1.csv examples/data_2.csv --report average-gdp
```

Скрипт выводит таблицу в консоль, отсортированную по убыванию среднего ВВП.

Пример вывода:

```text
| country       |   average_gdp |
|---------------|---------------|
| United States |      23923.7  |
| China         |      17810.3  |
| Germany       |       4138.33 |
```

## Тесты

```bash
pytest -q
```

## Как добавить новый отчёт

1. Добавить класс отчёта в `reports/reporting.py` с методом `generate(records)`.
2. Зарегистрировать его в `REPORT_REGISTRY`.
3. После этого новый отчёт станет доступен через `--report`.
