import csv
from math import ceil, sqrt

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lab_common import (
    LAGS,
    PLOTS_DIR,
    SAMPLE_SIZES,
    TABLES_DIR,
    autocorrelations,
    characteristics_by_size,
    fit_h2,
    format_number,
    generate_values,
    h2_density,
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


def save_form2(source, generated) -> None:
    rows = [["Характеристика", "Показатель", *map(str, SAMPLE_SIZES)]]
    for title, key, is_interval in ROWS:
        values = [generated[size][key] for size in SAMPLE_SIZES]
        shown = [format_number(value) for value in values]
        if is_interval:
            shown = [f"±{value}" for value in shown]
        deviations = [
            format_number(relative_deviation(generated[size][key], source[size][key]))
            for size in SAMPLE_SIZES
        ]
        rows.extend(([title, "Знач.", *shown], [title, "%", *deviations]))

    with (TABLES_DIR / "stage_7_form2.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        csv.writer(file, delimiter=";").writerows(rows)


def run() -> None:
    source_values = load_values()
    parameters = fit_h2(source_values)
    values = generate_values(parameters)
    source_results = characteristics_by_size(source_values)
    generated_results = characteristics_by_size(values)
    coefficients = autocorrelations(values)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    save_form2(source_results, generated_results)

    rows = [
        ["Сдвиг ЧП", *map(str, LAGS)],
        [
            "К-т АК для сгенер. ЧП",
            *(format_number(coefficients[lag]) for lag in LAGS),
        ],
    ]
    with (TABLES_DIR / "stage_7_autocorrelation.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        csv.writer(file, delimiter=";").writerows(rows)

    numbers = np.arange(1, len(values) + 1)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(numbers, values, color="#2563a6", linewidth=1.0)
    axis.set(xlabel="Номер значения", ylabel="Значение", xlim=(1, len(values)))
    axis.set_ylim(bottom=0)
    axis.grid(True, alpha=0.25)
    figure.tight_layout()
    figure.savefig(PLOTS_DIR / "generated_sequence.png", dpi=220, bbox_inches="tight")
    plt.close(figure)

    x_values = np.linspace(0, values.max() * 1.08, 1200)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.hist(
        values,
        bins=ceil(sqrt(len(values))),
        density=True,
        color="#5b9bd5",
        alpha=0.65,
        edgecolor="#202020",
        linewidth=0.8,
        label="Сгенерированная ЧП",
    )
    axis.plot(
        x_values,
        h2_density(x_values, parameters),
        color="#c23b22",
        linewidth=1.8,
        label="Плотность H_2",
    )
    axis.set(xlabel="Значение", ylabel="Плотность", xlim=(0, x_values[-1]))
    axis.grid(axis="y", alpha=0.25)
    axis.legend(loc="upper right")
    figure.tight_layout()
    figure.savefig(PLOTS_DIR / "generated_density.png", dpi=220, bbox_inches="tight")
    plt.close(figure)

    lags = np.array(LAGS)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(
        lags,
        [coefficients[lag] for lag in lags],
        color="#2563a6",
        linewidth=1.5,
    )
    axis.axhline(0, color="#202020", linewidth=0.8)
    axis.set(
        xlabel="Сдвиг",
        ylabel="Коэффициент автокорреляции",
        xlim=(0.5, 10.5),
        ylim=(-0.15, 0.15),
    )
    axis.set_xticks(lags)
    axis.grid(True, alpha=0.25)
    figure.tight_layout()
    figure.savefig(
        PLOTS_DIR / "generated_autocorrelation.png",
        dpi=220,
        bbox_inches="tight",
    )
    plt.close(figure)
    print("7. Сгенерированная последовательность исследована.")


if __name__ == "__main__":
    run()
