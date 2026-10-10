import csv
from pathlib import Path

from src.statistics import SAMPLE_SIZES, relative_deviation


ROWS = (
    ("Мат. ожидание", "mean", False),
    ("Дов. инт. (0,9)", "confidence_0.90", True),
    ("Дов. инт. (0,95)", "confidence_0.95", True),
    ("Дов. инт. (0,99)", "confidence_0.99", True),
    ("Дисперсия", "variance", False),
    ("С.к.о.", "standard_deviation", False),
    ("К-т вариации", "coefficient_of_variation", False),
)


def build_form1_rows(
    results: dict[int, dict[str, float]],
) -> list[list[str]]:
    rows = [["Характеристика", "Показатель", *map(str, SAMPLE_SIZES)]]

    for title, key, is_interval in ROWS:
        values = [results[size][key] for size in SAMPLE_SIZES]
        reference = results[300][key]

        formatted_values = [format_number(value) for value in values]
        if is_interval:
            formatted_values = [f"±{value}" for value in formatted_values]

        deviations = [
            format_number(relative_deviation(value, reference))
            for value in values
        ]

        rows.append([title, "Знач.", *formatted_values])
        rows.append([title, "%", *deviations])

    return rows


def save_form1(
    path: str | Path,
    results: dict[int, dict[str, float]],
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(build_form1_rows(results))


def save_summary(
    path: str | Path,
    results: dict[int, dict[str, float]],
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    values = results[300]
    values_20 = results[20]

    lines = [
        "Характеристики исходной последовательности для n = 300",
        f"Математическое ожидание: {format_number(values['mean'])}",
        f"Дисперсия: {format_number(values['variance'])}",
        f"Среднеквадратическое отклонение: {format_number(values['standard_deviation'])}",
        f"Коэффициент вариации: {format_number(values['coefficient_of_variation'])}",
        f"Полуширина доверительного интервала 0,90: ±{format_number(values['confidence_0.90'])}",
        f"Полуширина доверительного интервала 0,95: ±{format_number(values['confidence_0.95'])}",
        f"Полуширина доверительного интервала 0,99: ±{format_number(values['confidence_0.99'])}",
        "",
        "Вывод",
        (
            "Оценки математического ожидания, дисперсии и СКО при увеличении "
            "объёма выборки изменяются немонотонно."
        ),
        (
            "Для полной выборки математическое ожидание равно "
            f"{format_number(values['mean'])}, дисперсия — "
            f"{format_number(values['variance'])}, СКО — "
            f"{format_number(values['standard_deviation'])}."
        ),
        (
            "Полуширина доверительного интервала с вероятностью 0,95 "
            f"уменьшается с {format_number(values_20['confidence_0.95'])} "
            f"при n = 20 до {format_number(values['confidence_0.95'])} "
            "при n = 300, "
            "поэтому оценка среднего на большой выборке точнее."
        ),
        (
            "Коэффициент вариации полной выборки равен "
            f"{format_number(values['coefficient_of_variation'])}. Он больше "
            "единицы, что указывает на большой разброс значений относительно "
            "среднего."
        ),
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_number(value: float) -> str:
    return f"{value:.6f}"
