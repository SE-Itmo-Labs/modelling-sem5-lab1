import csv
from math import ceil, sqrt

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lab_common import (
    LAGS,
    PLOTS_DIR,
    TABLES_DIR,
    autocorrelations,
    characteristics,
    fit_h2,
    format_number,
    generate_values,
    h2_density,
    load_values,
    relative_deviation,
)


def run() -> None:
    source = load_values()
    parameters = fit_h2(source)
    generated = generate_values(parameters)
    source_ac = autocorrelations(source)
    generated_ac = autocorrelations(generated)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    # Процент не показывается, если исходная автокорреляция близка к нулю.
    deviations = [
        "—"
        if abs(source_ac[lag]) < 0.01
        else format_number(relative_deviation(generated_ac[lag], source_ac[lag]))
        for lag in LAGS
    ]
    with (TABLES_DIR / "form3.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        csv.writer(file, delimiter=";").writerows(
            [
                ["Сдвиг ЧП", *map(str, LAGS)],
                [
                    "К-т АК для задан. ЧП",
                    *(format_number(source_ac[lag]) for lag in LAGS),
                ],
                [
                    "К-т АК для сгенер. ЧП",
                    *(format_number(generated_ac[lag]) for lag in LAGS),
                ],
                ["Отклонение, %", *deviations],
            ]
        )

    x_values = np.linspace(0, source.max() * 1.05, 1200)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.hist(
        source,
        bins=ceil(sqrt(len(source))),
        density=True,
        color="#5b9bd5",
        alpha=0.65,
        edgecolor="#202020",
        linewidth=0.8,
        label="Исходная ЧП",
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
    figure.savefig(PLOTS_DIR / "density_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(figure)

    boundaries = np.linspace(
        min(source.min(), generated.min()),
        max(source.max(), generated.max()),
        ceil(sqrt(len(source))) + 1,
    )
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.hist(
        source,
        bins=boundaries,
        density=True,
        alpha=0.5,
        color="#2563a6",
        edgecolor="#202020",
        linewidth=0.7,
        label="Исходная ЧП",
    )
    axis.hist(
        generated,
        bins=boundaries,
        density=True,
        alpha=0.5,
        color="#e67e22",
        edgecolor="#202020",
        linewidth=0.7,
        label="Сгенерированная ЧП",
    )
    axis.set(xlabel="Значение", ylabel="Плотность")
    axis.grid(axis="y", alpha=0.25)
    axis.legend(loc="upper right")
    figure.tight_layout()
    figure.savefig(PLOTS_DIR / "histogram_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(figure)

    numbers = np.arange(1, len(source) + 1)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(numbers, source, linewidth=1.0, alpha=0.8, label="Исходная ЧП")
    axis.plot(
        numbers,
        generated,
        linewidth=1.0,
        alpha=0.8,
        label="Сгенерированная ЧП",
    )
    axis.set(xlabel="Номер значения", ylabel="Значение", xlim=(1, len(source)))
    axis.set_ylim(bottom=0)
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper left")
    figure.tight_layout()
    figure.savefig(PLOTS_DIR / "sequence_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(figure)

    lags = np.array(LAGS)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(
        lags,
        [source_ac[lag] for lag in lags],
        linewidth=1.5,
        label="Исходная ЧП",
    )
    axis.plot(
        lags,
        [generated_ac[lag] for lag in lags],
        linewidth=1.5,
        label="Сгенерированная ЧП",
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
    axis.legend(loc="lower right")
    figure.tight_layout()
    figure.savefig(
        PLOTS_DIR / "autocorrelation_comparison.png",
        dpi=220,
        bbox_inches="tight",
    )
    plt.close(figure)

    source_result = characteristics(source)
    generated_result = characteristics(generated)
    correlation = float(np.corrcoef(source, generated)[0, 1])
    print("8. Итоговое сравнение")
    print(f"Корреляция Пирсона: {correlation:.6f}")
    mean_error = relative_deviation(generated_result["mean"], source_result["mean"])
    variance_error = relative_deviation(
        generated_result["variance"], source_result["variance"]
    )
    print(f"Отклонение среднего: {mean_error:.2f}%")
    print(f"Отклонение дисперсии: {variance_error:.2f}%")


if __name__ == "__main__":
    run()
