from importlib import import_module

import numpy as np
import pytest

from lab_common import (
    H2Parameters,
    autocorrelation,
    autocorrelations,
    characteristics,
    characteristics_by_size,
    empirical_moments,
    fit_h2,
    generate_values,
    h2_density,
    load_values,
    relative_deviation,
    theoretical_moments,
)


def test_characteristics_for_simple_sample() -> None:
    result = characteristics(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    assert result["mean"] == pytest.approx(3.0)
    assert result["variance"] == pytest.approx(2.5)
    assert result["deviation"] == pytest.approx(np.sqrt(2.5))
    assert result["confidence_0.95"] == pytest.approx(1.385929, rel=1e-6)


def test_variant_29_results() -> None:
    values = load_values()
    result = characteristics_by_size(values)[300]
    assert len(values) == 300
    assert result["mean"] == pytest.approx(19.62616)
    assert result["variance"] == pytest.approx(1107.974782, rel=1e-9)
    assert result["variation"] == pytest.approx(1.696015, rel=1e-6)


def test_relative_deviation() -> None:
    assert relative_deviation(90, 100) == pytest.approx(10)
    assert relative_deviation(110, 100) == pytest.approx(10)
    with pytest.raises(ValueError, match="нулевого"):
        relative_deviation(1, 0)


def test_autocorrelation() -> None:
    alternating = np.array([1.0, -1.0, 1.0, -1.0])
    assert autocorrelation(alternating, 1) == pytest.approx(-0.75)
    assert autocorrelation(alternating, 2) == pytest.approx(0.5)
    assert autocorrelations(load_values())[1] == pytest.approx(0.0168839649)


def test_h2_reproduces_two_moments() -> None:
    values = load_values()
    empirical = empirical_moments(values)
    parameters = fit_h2(values)
    theoretical = theoretical_moments(parameters)
    assert parameters == pytest.approx(H2Parameters(0.25, 52.468862, 8.678593), rel=1e-7)
    assert theoretical["mean"] == pytest.approx(empirical["mean"])
    assert theoretical["second_moment"] == pytest.approx(empirical["second_moment"])


def test_generator_is_reproducible() -> None:
    parameters = fit_h2(load_values())
    first = generate_values(parameters)
    second = generate_values(parameters)
    assert np.array_equal(first, second)
    assert len(first) == 300
    assert np.all(first >= 0)


def test_h2_density_decreases() -> None:
    density = h2_density(np.array([0.0, 1.0, 2.0]), fit_h2(load_values()))
    assert np.all(density > 0)
    assert np.all(np.diff(density) < 0)


def test_every_script_has_run_function() -> None:
    for number, name in enumerate(
        (
            "statistics",
            "sequence_plot",
            "autocorrelation",
            "histogram",
            "distribution",
            "generator",
            "generated_analysis",
            "comparison",
        ),
        start=1,
    ):
        assert callable(import_module(f"{number}_{name}").run)
