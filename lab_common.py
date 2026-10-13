from math import sqrt
from pathlib import Path
from typing import Generator, NamedTuple

import numpy as np


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "29_data.txt"
RESULTS_DIR = ROOT / "results"
PLOTS_DIR = RESULTS_DIR / "plots"
TABLES_DIR = RESULTS_DIR / "tables"

VARIANT = 29
VALUES_COUNT = 300
SAMPLE_SIZES = (10, 20, 50, 100, 200, 300)
CONFIDENCE_LEVELS = (0.90, 0.95, 0.99)
CONFIDENCE_COEFFICIENTS = {0.90: 1.643, 0.95: 1.960, 0.99: 2.576}
LAGS = tuple(range(1, 11))
Q = 0.25
SEED = 29


class H2Parameters(NamedTuple):
    q: float
    t1: float
    t2: float


def load_values() -> np.ndarray:
    tokens = DATA_FILE.read_text(encoding="utf-8-sig").split()
    if not tokens or int(tokens[0]) != VARIANT:
        raise ValueError("В файле должен быть указан вариант 29.")

    values = np.array([float(token.replace(",", ".")) for token in tokens[1:]])
    if len(values) != VALUES_COUNT:
        raise ValueError("В исходной последовательности должно быть 300 значений.")
    if not np.all(np.isfinite(values)) or np.any(values < 0):
        raise ValueError("Все исходные значения должны быть конечными и неотрицательными.")
    return values


def characteristics(values: np.ndarray) -> dict[str, float]:
    mean = float(np.mean(values))
    variance = float(np.var(values, ddof=1))
    deviation = sqrt(variance)
    result = {
        "mean": mean,
        "variance": variance,
        "deviation": deviation,
        "variation": deviation / abs(mean),
    }
    for probability in CONFIDENCE_LEVELS:
        coefficient = CONFIDENCE_COEFFICIENTS[probability]
        result[f"confidence_{probability:.2f}"] = float(
            coefficient * deviation / sqrt(len(values))
        )
    return result


def characteristics_by_size(values: np.ndarray) -> dict[int, dict[str, float]]:
    return {size: characteristics(values[:size]) for size in SAMPLE_SIZES}


def relative_deviation(value: float, reference: float) -> float:
    if reference == 0:
        raise ValueError("Нельзя рассчитать отклонение от нулевого значения.")
    return abs(value - reference) / abs(reference) * 100


def autocorrelation(values: np.ndarray, lag: int) -> float:
    centered = values - np.mean(values)
    # Знаменатель общий для всех сдвигов и соответствует формуле из отчёта
    return float(np.sum(centered[:-lag] * centered[lag:]) / np.sum(centered**2))


def autocorrelations(values: np.ndarray) -> dict[int, float]:
    return {lag: autocorrelation(values, lag) for lag in LAGS}


def empirical_moments(values: np.ndarray) -> dict[str, float]:
    mean = float(np.mean(values))
    second_moment = float(np.mean(values**2))
    # В методе моментов используется делитель n, а не выборочная дисперсия с n - 1
    variance = second_moment - mean**2
    return {
        "mean": mean,
        "second_moment": second_moment,
        "variance": variance,
        "variation": sqrt(variance) / mean,
    }


def fit_h2(values: np.ndarray) -> H2Parameters:
    moments = empirical_moments(values)
    mean = moments["mean"]
    variation = moments["variation"]
    if variation <= 1:
        raise ValueError("Для закона H2 коэффициент вариации должен быть больше 1.")

    maximum_q = 2 / (1 + variation**2)
    if Q > maximum_q:
        raise ValueError("Выбранное значение q не входит в допустимый диапазон.")

    excess = variation**2 - 1
    t1 = mean * (1 + sqrt((1 - Q) * excess / (2 * Q)))
    t2 = mean * (1 - sqrt(Q * excess / (2 * (1 - Q))))
    return H2Parameters(Q, t1, t2)


def theoretical_moments(parameters: H2Parameters) -> dict[str, float]:
    q, t1, t2 = parameters
    mean = q * t1 + (1 - q) * t2
    second_moment = 2 * (q * t1**2 + (1 - q) * t2**2)
    variance = second_moment - mean**2
    return {
        "mean": mean,
        "second_moment": second_moment,
        "variance": variance,
        "variation": sqrt(variance) / mean,
    }


def h2_density(values: np.ndarray, parameters: H2Parameters) -> np.ndarray:
    q, t1, t2 = parameters
    return q / t1 * np.exp(-values / t1) + (1 - q) / t2 * np.exp(-values / t2)


def generate_values(parameters: H2Parameters) -> np.ndarray:

    generator : Generator = np.random.default_rng(SEED) # задаем значения по сиду
    phase_numbers = generator.random(VALUES_COUNT)
    value_numbers = generator.random(VALUES_COUNT)

    # Первое число выбирает фазу, второе преобразуется в экспоненциальную величину
    phase_means = np.where(phase_numbers < parameters.q, parameters.t1, parameters.t2)
    return -phase_means * np.log1p(-value_numbers)


def format_number(value: float) -> str:
    return f"{value:.6f}"
