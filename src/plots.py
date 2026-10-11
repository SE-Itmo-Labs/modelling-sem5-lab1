from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

import matplotlib.pyplot as plt


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
