from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.statistics import AUTOCORRELATION_LAGS


def save_source_sequence_plot(path: Path, values: np.ndarray) -> None:
    """Save a plot of the source sequence."""
    sample = np.asarray(values, dtype=float)
    if sample.ndim != 1 or sample.size < 2:
        raise ValueError("Для построения графика требуется не менее двух значений")

    numbers = np.arange(1, sample.size + 1)

    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(
        numbers,
        sample,
        color="#2563a6",
        linewidth=1.0,
        label="Исходная последовательность",
    )
    axis.set_xlabel("Номер значения")
    axis.set_ylabel("Значение")
    axis.set_xlim(1, sample.size)
    axis.set_ylim(bottom=0)
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper left")
    figure.tight_layout()
    figure.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def save_stage_2_summary(path: Path, values: np.ndarray) -> None:
    """Save the stage 2 report conclusion."""
    sample = np.asarray(values, dtype=float)
    if sample.ndim != 1 or sample.size < 2:
        raise ValueError("Для анализа требуется не менее двух значений")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "Этап 2. Анализ характера исходной последовательности\n"
        "Вывод: выраженный возрастающий или убывающий тренд отсутствует; "
        "явная периодичность по графику не обнаружена.\n",
        encoding="utf-8",
    )


def save_autocorrelation_plot(
    path: Path,
    values: dict[int, float],
) -> None:
    """Save source-sequence autocorrelations for lags 1 through 10."""
    lags = np.asarray(AUTOCORRELATION_LAGS)
    coefficients = np.asarray([values[lag] for lag in lags])

    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(lags, coefficients, color="#2563a6", linewidth=1.5)
    axis.axhline(0, color="#202020", linewidth=0.8)
    axis.set_xlabel("Сдвиг")
    axis.set_ylabel("Коэффициент автокорреляции")
    axis.set_xticks(lags)
    axis.set_xlim(0.5, 10.5)
    axis.set_ylim(-0.15, 0.15)
    axis.grid(True, alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def save_source_histogram_plot(
    path: Path,
    values: np.ndarray,
    boundaries: np.ndarray,
) -> None:
    """Save an absolute-frequency histogram of the source sequence."""
    sample = np.asarray(values, dtype=float)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.hist(
        sample,
        bins=boundaries,
        color="#5b9bd5",
        edgecolor="#202020",
        linewidth=0.8,
    )
    axis.set_xlabel("Значение")
    axis.set_ylabel("Частота")
    axis.set_xlim(boundaries[0], boundaries[-1])
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(figure)
