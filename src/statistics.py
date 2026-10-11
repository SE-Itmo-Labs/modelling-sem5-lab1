from math import ceil, sqrt

import numpy as np
from scipy.stats import t


SAMPLE_SIZES = (10, 20, 50, 100, 200, 300)
CONFIDENCE_LEVELS = (0.90, 0.95, 0.99)
AUTOCORRELATION_LAGS = tuple(range(1, 11))


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


def autocorrelation(values: np.ndarray, lag: int) -> float:
    """Calculate sample autocorrelation for a positive lag."""
    sample = np.asarray(values, dtype=float)
    if sample.ndim != 1 or sample.size < 2:
        raise ValueError("Для автокорреляции требуется не менее двух значений.")
    if lag < 1 or lag >= sample.size:
        raise ValueError("Сдвиг должен быть от 1 до n - 1.")

    centered = sample - np.mean(sample)
    denominator = float(np.sum(centered**2))
    if denominator == 0:
        raise ValueError("Автокорреляция не определена для постоянной выборки.")

    numerator = float(np.sum(centered[:-lag] * centered[lag:]))
    return numerator / denominator


def calculate_autocorrelations(values: np.ndarray) -> dict[int, float]:
    return {
        lag: autocorrelation(values, lag)
        for lag in AUTOCORRELATION_LAGS
    }


def calculate_histogram(
    values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate histogram frequencies using ceil(sqrt(n)) equal-width bins."""
    sample = np.asarray(values, dtype=float)
    if sample.ndim != 1 or sample.size < 2:
        raise ValueError("Для гистограммы требуется не менее двух значений.")

    bin_count = ceil(sqrt(sample.size))
    frequencies, boundaries = np.histogram(sample, bins=bin_count)
    return boundaries, frequencies


def correlation_coefficient(first: np.ndarray, second: np.ndarray) -> float:
    first_sample = np.asarray(first, dtype=float)
    second_sample = np.asarray(second, dtype=float)
    if first_sample.ndim != 1 or second_sample.ndim != 1:
        raise ValueError("Последовательности должны быть одномерными.")
    if first_sample.size != second_sample.size or first_sample.size < 2:
        raise ValueError("Последовательности должны иметь одинаковую длину не менее 2.")
    if np.std(first_sample) == 0 or np.std(second_sample) == 0:
        raise ValueError("Корреляция не определена для постоянной последовательности.")
    return float(np.corrcoef(first_sample, second_sample)[0, 1])


def confidence_key(probability: float) -> str:
    return f"confidence_{probability:.2f}"
