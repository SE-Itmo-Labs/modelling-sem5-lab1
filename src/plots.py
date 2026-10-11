from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from src.hyperexponential import (
    HyperexponentialParameters,
    hyperexponential_density,
)
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


def save_generator_algorithm_plot(path: Path) -> None:
    """Save a compact flowchart of the H2 generation algorithm."""
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(7, 8.5))
    axis.set_xlim(0, 10)
    axis.set_ylim(0, 14)
    axis.axis("off")

    steps = (
        (12.7, "Начало", 2.6),
        (10.9, "Задать q, t₁, t₂, seed и n = 300", 6.8),
        (9.1, "Сгенерировать U₀, U₁ ∈ (0; 1)", 6.8),
        (7.3, "t = t₁, если U₀ < q; иначе t = t₂", 7.4),
        (5.5, "Xᵢ = −t · ln(1 − U₁)", 5.8),
        (3.7, "Повторить для i = 1, …, 300", 6.2),
        (1.9, "Сохранить последовательность", 5.6),
        (0.4, "Конец", 2.6),
    )
    for y, label, width in steps:
        height = 0.9
        left = 5 - width / 2
        box = FancyBboxPatch(
            (left, y),
            width,
            height,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor="#edf4fb",
            edgecolor="#2563a6",
            linewidth=1.4,
        )
        axis.add_patch(box)
        axis.text(5, y + height / 2, label, ha="center", va="center", fontsize=10)

    for current, following in zip(steps[:-1], steps[1:]):
        current_y = current[0]
        following_y = following[0]
        axis.annotate(
            "",
            xy=(5, following_y + 0.95),
            xytext=(5, current_y),
            arrowprops={"arrowstyle": "->", "color": "#202020", "linewidth": 1.2},
        )

    figure.tight_layout()
    figure.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def save_generated_sequence_plot(path: Path, values: np.ndarray) -> None:
    """Save the generated sequence in observation order."""
    sample = np.asarray(values, dtype=float)
    numbers = np.arange(1, sample.size + 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.plot(numbers, sample, color="#2563a6", linewidth=1.0)
    axis.set_xlabel("Номер значения")
    axis.set_ylabel("Значение")
    axis.set_xlim(1, sample.size)
    axis.set_ylim(bottom=0)
    axis.grid(True, alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def save_generated_density_plot(
    path: Path,
    values: np.ndarray,
    parameters: HyperexponentialParameters,
) -> None:
    """Save a normalized generated histogram with the fitted H2 density."""
    sample = np.asarray(values, dtype=float)
    bin_count = int(np.ceil(np.sqrt(sample.size)))
    x_values = np.linspace(0, sample.max() * 1.08, 1200)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 4.8))
    axis.hist(
        sample,
        bins=bin_count,
        density=True,
        color="#5b9bd5",
        alpha=0.65,
        edgecolor="#202020",
        linewidth=0.8,
        label="Сгенерированная ЧП",
    )
    axis.plot(
        x_values,
        hyperexponential_density(x_values, parameters),
        color="#c23b22",
        linewidth=1.8,
        label="Плотность H₂",
    )
    axis.set_xlabel("Значение")
    axis.set_ylabel("Плотность")
    axis.set_xlim(0, x_values[-1])
    axis.grid(axis="y", alpha=0.25)
    axis.legend(loc="upper right")
    figure.tight_layout()
    figure.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(figure)
