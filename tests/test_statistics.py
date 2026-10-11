from pathlib import Path

import numpy as np
import pytest

from src.data_io import load_sequence
from src.statistics import (
    autocorrelation,
    calculate_autocorrelations,
    calculate_characteristics,
    calculate_for_sample_sizes,
    calculate_histogram,
    relative_deviation,
)


ROOT = Path(__file__).resolve().parents[1]


def test_characteristics_for_simple_sample() -> None:
    result = calculate_characteristics(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))

    assert result["mean"] == pytest.approx(3.0)
    assert result["variance"] == pytest.approx(2.5)
    assert result["standard_deviation"] == pytest.approx(np.sqrt(2.5))
    assert result["coefficient_of_variation"] == pytest.approx(np.sqrt(2.5) / 3)
    assert result["confidence_0.95"] == pytest.approx(1.963243, rel=1e-6)


def test_relative_deviation() -> None:
    assert relative_deviation(90, 100) == pytest.approx(10)
    assert relative_deviation(110, 100) == pytest.approx(10)
    assert relative_deviation(100, 100) == pytest.approx(0)


def test_reference_value_cannot_be_zero() -> None:
    with pytest.raises(ValueError, match="нулевого"):
        relative_deviation(1, 0)


def test_variant_29_full_sample() -> None:
    values = load_sequence(ROOT / "data" / "29_data.txt")
    result = calculate_for_sample_sizes(values)[300]

    assert len(values) == 300
    assert result["mean"] == pytest.approx(19.62616)
    assert result["variance"] == pytest.approx(1107.974782, rel=1e-9)
    assert result["standard_deviation"] == pytest.approx(33.286255, rel=1e-8)
    assert result["coefficient_of_variation"] == pytest.approx(1.696015, rel=1e-6)


def test_wrong_variant_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "wrong_variant.txt"
    path.write_text("28\n" + "\n".join(["1"] * 300), encoding="utf-8")

    with pytest.raises(ValueError, match="Ожидался вариант 29"):
        load_sequence(path)


def test_autocorrelation_for_alternating_sequence() -> None:
    values = np.array([1.0, -1.0, 1.0, -1.0])

    assert autocorrelation(values, 1) == pytest.approx(-0.75)
    assert autocorrelation(values, 2) == pytest.approx(0.5)


def test_variant_29_autocorrelations() -> None:
    values = load_sequence(ROOT / "data" / "29_data.txt")
    result = calculate_autocorrelations(values)

    assert tuple(result) == tuple(range(1, 11))
    assert result[1] == pytest.approx(0.0168839649)


def test_histogram_uses_square_root_rule() -> None:
    boundaries, frequencies = calculate_histogram(np.arange(1.0, 301.0))

    assert len(frequencies) == 18
    assert len(boundaries) == 19
    assert int(frequencies.sum()) == 300
