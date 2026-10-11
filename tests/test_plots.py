from pathlib import Path

import numpy as np

from src.plots import (
    save_autocorrelation_plot,
    save_generator_algorithm_plot,
    save_source_histogram_plot,
    save_source_sequence_plot,
)


def test_source_sequence_plot_is_saved(tmp_path: Path) -> None:
    path = tmp_path / "sequence.png"

    save_source_sequence_plot(path, np.array([2.0, 1.0, 3.0, 2.0]))

    assert path.is_file()
    assert path.stat().st_size > 0


def test_autocorrelation_plot_is_saved(tmp_path: Path) -> None:
    path = tmp_path / "autocorrelation.png"
    values = {lag: 0.01 * lag for lag in range(1, 11)}

    save_autocorrelation_plot(path, values)

    assert path.is_file()
    assert path.stat().st_size > 0


def test_histogram_plot_is_saved(tmp_path: Path) -> None:
    path = tmp_path / "histogram.png"
    values = np.arange(1.0, 21.0)
    boundaries = np.linspace(1.0, 21.0, 6)

    save_source_histogram_plot(path, values, boundaries)

    assert path.is_file()
    assert path.stat().st_size > 0


def test_generator_algorithm_plot_is_saved(tmp_path: Path) -> None:
    path = tmp_path / "generator_algorithm.png"

    save_generator_algorithm_plot(path)

    assert path.is_file()
    assert path.stat().st_size > 0
