import numpy as np
import pytest

from src.hyperexponential import (
    empirical_moments,
    fit_hyperexponential,
    generate_hyperexponential,
    hyperexponential_density,
    theoretical_moments,
)


def test_h2_parameters_reproduce_first_two_moments() -> None:
    values = np.array([1.0, 1.0, 1.0, 10.0])
    empirical = empirical_moments(values)
    parameters = fit_hyperexponential(values, probability=0.25)
    theoretical = theoretical_moments(parameters)

    assert parameters.phase_1_mean > 0
    assert parameters.phase_2_mean > 0
    assert theoretical["mean"] == pytest.approx(empirical["mean"])
    assert theoretical["second_raw_moment"] == pytest.approx(
        empirical["second_raw_moment"]
    )


def test_h2_rejects_probability_outside_admissible_range() -> None:
    values = np.array([1.0, 1.0, 1.0, 10.0])

    with pytest.raises(ValueError, match="не больше"):
        fit_hyperexponential(values, probability=0.9)


def test_h2_generator_is_reproducible_and_nonnegative() -> None:
    parameters = fit_hyperexponential(
        np.array([1.0, 1.0, 1.0, 10.0]),
        probability=0.25,
    )

    first = generate_hyperexponential(parameters, size=300, seed=29)
    second = generate_hyperexponential(parameters, size=300, seed=29)

    assert np.array_equal(first, second)
    assert len(first) == 300
    assert np.all(np.isfinite(first))
    assert np.all(first >= 0)


def test_h2_density_is_positive_and_decreasing() -> None:
    parameters = fit_hyperexponential(
        np.array([1.0, 1.0, 1.0, 10.0]),
        probability=0.25,
    )
    density = hyperexponential_density(np.array([0.0, 1.0, 2.0]), parameters)

    assert np.all(density > 0)
    assert np.all(np.diff(density) < 0)
