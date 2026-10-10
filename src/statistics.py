from math import sqrt

import numpy as np
from scipy.stats import t


SAMPLE_SIZES = (10, 20, 50, 100, 200, 300)
CONFIDENCE_LEVELS = (0.90, 0.95, 0.99)


def calculate_characteristics(values: np.ndarray) -> dict[str, float]:
    sample = np.asarray(values, dtype=float)
    if len(sample) < 2:
        raise ValueError("Для расчёта характеристик нужно минимум два значения.")

    mean = float(np.mean(sample))
    variance = float(np.var(sample, ddof=1))
    standard_deviation = sqrt(variance)

    if mean == 0:
        raise ValueError("Коэффициент вариации не определён при нулевом среднем.")

    result = {
        "mean": mean,
        "variance": variance,
        "standard_deviation": standard_deviation,
        "coefficient_of_variation": standard_deviation / abs(mean),
    }

    for probability in CONFIDENCE_LEVELS:
        quantile = t.ppf((1 + probability) / 2, len(sample) - 1)
        result[confidence_key(probability)] = float(
            quantile * standard_deviation / sqrt(len(sample))
        )

    return result


def calculate_for_sample_sizes(values: np.ndarray) -> dict[int, dict[str, float]]:
    sample = np.asarray(values, dtype=float)
    if len(sample) < max(SAMPLE_SIZES):
        raise ValueError("Для расчёта таблицы требуется 300 значений.")

    return {
        size: calculate_characteristics(sample[:size])
        for size in SAMPLE_SIZES
    }


def relative_deviation(value: float, reference: float) -> float:
    if reference == 0:
        raise ValueError("Нельзя рассчитать отклонение от нулевого значения.")
    return abs(value - reference) / abs(reference) * 100


def confidence_key(probability: float) -> str:
    return f"confidence_{probability:.2f}"
