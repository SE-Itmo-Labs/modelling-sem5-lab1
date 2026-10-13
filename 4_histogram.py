import csv
from math import ceil, sqrt

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lab_common import PLOTS_DIR, TABLES_DIR, format_number, load_values


def run() -> None:
    values = load_values()
    frequencies, boundaries = np.histogram(values, bins=ceil(sqrt(len(values))))

    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    rows = [["№", "Левая граница", "Правая граница", "Частота"]]
    intervals = zip(boundaries[:-1], boundaries[1:], frequencies)

    for number, (left, right, frequency) in enumerate(intervals, start=1):
        rows.append([number, format_number(left), format_number(right), int(frequency)])
    with (TABLES_DIR / "stage_4_histogram.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        csv.writer(file, delimiter=";").writerows(rows)

    figure, axis = plt.subplots(figsize=(10, 4.8))

    axis.hist(
        values,
        bins=boundaries,
        color="#5b9bd5",
        edgecolor="#202020",
        linewidth=0.8,
    )
    axis.set(
        xlabel="Значение",
        ylabel="Частота",
        xlim=(boundaries[0], boundaries[-1]),
    )

    axis.grid(axis="y", alpha=0.25)

    figure.tight_layout()
    figure.savefig(PLOTS_DIR / "source_histogram.png", dpi=220, bbox_inches="tight")
    
    plt.close(figure)
    print(f"4. Гистограмма построена по {len(frequencies)} интервалам.")


if __name__ == "__main__":
    run()
