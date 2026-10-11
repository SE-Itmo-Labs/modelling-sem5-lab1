import numpy as np
import pytest

from src.hyperexponential import (
    empirical_moments,
    fit_hyperexponential,
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
