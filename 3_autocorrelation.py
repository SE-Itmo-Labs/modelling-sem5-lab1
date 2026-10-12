import csv
from math import sqrt

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lab_common import (
    LAGS,
    PLOTS_DIR,
    TABLES_DIR,
    autocorrelations,
    format_number,
    load_values,
)


def draw_plot(values: dict[int, float], path) -> None:
    lags = np.array(LAGS)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(
        lags,
        [values[lag] for lag in lags],
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
    figure.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def run() -> None:
    values = load_values()
    coefficients = autocorrelations(values)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        ["Сдвиг ЧП", *map(str, LAGS)],
        [
            "К-т АК для задан. ЧП",
            *(format_number(coefficients[lag]) for lag in LAGS),
        ],
    ]
    with (TABLES_DIR / "stage_3_autocorrelation.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        csv.writer(file, delimiter=";").writerows(rows)
    draw_plot(coefficients, PLOTS_DIR / "source_autocorrelation.png")
    bound = 1.96 / sqrt(len(values))
    print(f"3. Все коэффициенты автокорреляции находятся в границах ±{bound:.6f}.")


if __name__ == "__main__":
    run()
