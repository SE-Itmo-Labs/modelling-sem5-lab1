import csv

from lab_common import (
    SAMPLE_SIZES,
    TABLES_DIR,
    characteristics_by_size,
    format_number,
    load_values,
    relative_deviation,
)


ROWS = (
    ("Мат. ожидание", "mean", False),
    ("Дов. инт. (0,9)", "confidence_0.90", True),
    ("Дов. инт. (0,95)", "confidence_0.95", True),
    ("Дов. инт. (0,99)", "confidence_0.99", True),
    ("Дисперсия", "variance", False),
    ("С.к.о.", "deviation", False),
    ("К-т вариации", "variation", False),
)


def form_rows(results: dict[int, dict[str, float]]) -> list[list[str]]:
    rows = [["Характеристика", "Показатель", *map(str, SAMPLE_SIZES)]]
    for title, key, is_interval in ROWS:
        values = [results[size][key] for size in SAMPLE_SIZES]
        shown = [format_number(value) for value in values]
        if is_interval:
            shown = [f"±{value}" for value in shown]
        deviations = [
            format_number(relative_deviation(value, results[300][key]))
            for value in values
        ]
        rows.extend(([title, "Знач.", *shown], [title, "%", *deviations]))
    return rows


def run() -> None:
    results = characteristics_by_size(load_values())
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    with (TABLES_DIR / "stage_1_data.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        csv.writer(file, delimiter=";").writerows(form_rows(results))

    full = results[300]
    print("1. Статистические характеристики")
    print(f"Среднее: {full['mean']:.6f}")
    print(f"Дисперсия: {full['variance']:.6f}")
    print(f"СКО: {full['deviation']:.6f}")
    print(f"Коэффициент вариации: {full['variation']:.6f}")


if __name__ == "__main__":
    run()
