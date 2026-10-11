from dataclasses import dataclass
from math import sqrt
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class HyperexponentialParameters:
    probability: float
    phase_1_mean: float
    phase_2_mean: float

    @property
    def phase_1_rate(self) -> float:
        return 1 / self.phase_1_mean

    @property
    def phase_2_rate(self) -> float:
        return 1 / self.phase_2_mean


def empirical_moments(values: np.ndarray) -> dict[str, float]:
    """Return moments with divisor n, as required by the method of moments."""
    sample = np.asarray(values, dtype=float)
    if sample.ndim != 1 or sample.size < 2:
        raise ValueError("Для расчёта моментов требуется не менее двух значений.")

    mean = float(np.mean(sample))
    second_raw_moment = float(np.mean(sample**2))
    variance = second_raw_moment - mean**2
    if mean <= 0 or variance <= 0:
        raise ValueError("Среднее и дисперсия должны быть положительными.")

    return {
        "mean": mean,
        "second_raw_moment": second_raw_moment,
        "variance": variance,
        "coefficient_of_variation": sqrt(variance) / mean,
    }


def fit_hyperexponential(
    values: np.ndarray,
    probability: float = 0.25,
) -> HyperexponentialParameters:
    """Fit an H2 distribution to the first two empirical moments."""
    moments = empirical_moments(values)
    mean = moments["mean"]
    variation = moments["coefficient_of_variation"]
    if variation <= 1:
        raise ValueError("Гиперэкспоненциальный закон требует коэффициент вариации > 1.")
    if not 0 < probability < 1:
        raise ValueError("Вероятность q должна находиться между 0 и 1.")

    maximum_probability = 2 / (1 + variation**2)
    if probability > maximum_probability:
        raise ValueError(
            f"Вероятность q должна быть не больше {maximum_probability:.6f}."
        )

    excess = variation**2 - 1
    phase_1_mean = mean * (
        1 + sqrt((1 - probability) * excess / (2 * probability))
    )
    phase_2_mean = mean * (
        1 - sqrt(probability * excess / (2 * (1 - probability)))
    )
    return HyperexponentialParameters(
        probability=probability,
        phase_1_mean=phase_1_mean,
        phase_2_mean=phase_2_mean,
    )


def theoretical_moments(
    parameters: HyperexponentialParameters,
) -> dict[str, float]:
    q = parameters.probability
    t_1 = parameters.phase_1_mean
    t_2 = parameters.phase_2_mean
    mean = q * t_1 + (1 - q) * t_2
    second_raw_moment = 2 * (q * t_1**2 + (1 - q) * t_2**2)
    variance = second_raw_moment - mean**2
    return {
        "mean": mean,
        "second_raw_moment": second_raw_moment,
        "variance": variance,
        "coefficient_of_variation": sqrt(variance) / mean,
    }


def generate_hyperexponential(
    parameters: HyperexponentialParameters,
    size: int,
    seed: int,
) -> np.ndarray:
    """Generate an H2 sample by phase selection and inverse transformation."""
    if size < 1:
        raise ValueError("Размер последовательности должен быть положительным.")

    generator = np.random.default_rng(seed)
    phase_uniforms = generator.random(size)
    value_uniforms = generator.random(size)
    phase_means = np.where(
        phase_uniforms < parameters.probability,
        parameters.phase_1_mean,
        parameters.phase_2_mean,
    )
    return -phase_means * np.log1p(-value_uniforms)


def save_generated_sequence(
    path: str | Path,
    values: np.ndarray,
    parameters: HyperexponentialParameters,
    seed: int,
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"seed={seed}; q={parameters.probability:.6f}; "
        f"t1={parameters.phase_1_mean:.6f}; t2={parameters.phase_2_mean:.6f}"
    )
    np.savetxt(output_path, values, fmt="%.10f", header=header, encoding="utf-8")
