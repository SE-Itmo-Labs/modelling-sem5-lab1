import csv
from pathlib import Path

from src.hyperexponential import HyperexponentialParameters
from src.statistics import AUTOCORRELATION_LAGS, SAMPLE_SIZES, relative_deviation


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
        f"Полуширина ДИ 0,90: +-{format_number(values['confidence_0.90'])}",
        f"Полуширина ДИ 0,95: +-{format_number(values['confidence_0.95'])}",
        f"Полуширина ДИ 0,99: +-{format_number(values['confidence_0.99'])}",
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


def save_source_autocorrelations(
    path: str | Path,
    values: dict[int, float],
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ["Сдвиг ЧП", *map(str, AUTOCORRELATION_LAGS)],
        [
            "К-т АК для задан. ЧП",
            *(format_number(values[lag]) for lag in AUTOCORRELATION_LAGS),
        ],
    ]
    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        csv.writer(file, delimiter=";").writerows(rows)


def save_stage_3_summary(
    path: str | Path,
    values: dict[int, float],
    confidence_bound: float,
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    maximum_lag = max(values, key=lambda lag: abs(values[lag]))
    significant_lags = [
        lag for lag, value in values.items() if abs(value) > confidence_bound
    ]
    significance = (
        "нет" if not significant_lags else ", ".join(map(str, significant_lags))
    )
    lines = [
        "Этап 3. Автокорреляционный анализ",
        f"Ориентировочные границы: ±{confidence_bound:.6f}",
        (
            "Максимальный по модулю коэффициент: "
            f"r({maximum_lag}) = {values[maximum_lag]:.6f}"
        ),
        f"Сдвиги за границами: {significance}",
        (
            "Вывод: статистически заметная автокорреляция на сдвигах 1-10 "
            "не обнаружена; последовательность можно считать случайной."
            if not significant_lags
            else "Вывод: обнаружены коэффициенты за ориентировочными границами."
        ),
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_source_histogram(
    path: str | Path,
    boundaries: object,
    frequencies: object,
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [["№", "Левая граница", "Правая граница", "Частота"]]
    for number, (left, right, frequency) in enumerate(
        zip(boundaries[:-1], boundaries[1:], frequencies),
        start=1,
    ):
        rows.append(
            [
                str(number),
                format_number(float(left)),
                format_number(float(right)),
                str(int(frequency)),
            ]
        )

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        csv.writer(file, delimiter=";").writerows(rows)


def save_stage_4_summary(
    path: str | Path,
    boundaries: object,
    frequencies: object,
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    maximum_index = max(range(len(frequencies)), key=lambda index: frequencies[index])
    lines = [
        "Этап 4. Гистограмма распределения частот",
        f"Количество интервалов: {len(frequencies)}",
        f"Ширина интервала: {float(boundaries[1] - boundaries[0]):.6f}",
        (
            "Максимальная частота: "
            f"{int(frequencies[maximum_index])} в интервале "
            f"[{float(boundaries[maximum_index]):.6f}; "
            f"{float(boundaries[maximum_index + 1]):.6f})"
        ),
        (
            "Вывод: основная масса наблюдений сосредоточена в области малых "
            "значений; распределение имеет выраженную правостороннюю "
            "асимметрию и длинный правый хвост."
        ),
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_stage_5_summary(
    path: str | Path,
    empirical: dict[str, float],
    parameters: HyperexponentialParameters,
    theoretical: dict[str, float],
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    maximum_probability = 2 / (
        1 + empirical["coefficient_of_variation"] ** 2
    )
    lines = [
        "Этап 5. Параметры гиперэкспоненциального распределения H2",
        f"Эмпирическое среднее: {empirical['mean']:.6f}",
        f"Эмпирический второй начальный момент: {empirical['second_raw_moment']:.6f}",
        f"Моментная дисперсия: {empirical['variance']:.6f}",
        f"Моментный коэффициент вариации: {empirical['coefficient_of_variation']:.6f}",
        f"Допустимая верхняя граница q: {maximum_probability:.6f}",
        f"Выбранная вероятность q: {parameters.probability:.6f}",
        f"Среднее первой фазы t1: {parameters.phase_1_mean:.6f}",
        f"Среднее второй фазы t2: {parameters.phase_2_mean:.6f}",
        f"Интенсивность первой фазы lambda1: {parameters.phase_1_rate:.6f}",
        f"Интенсивность второй фазы lambda2: {parameters.phase_2_rate:.6f}",
        f"Теоретическое среднее H2: {theoretical['mean']:.6f}",
        f"Теоретический второй начальный момент H2: {theoretical['second_raw_moment']:.6f}",
        f"Теоретическая дисперсия H2: {theoretical['variance']:.6f}",
        f"Теоретический коэффициент вариации H2: {theoretical['coefficient_of_variation']:.6f}",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_number(value: float) -> str:
    return f"{value:.6f}"
