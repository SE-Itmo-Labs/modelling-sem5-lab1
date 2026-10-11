from pathlib import Path

import numpy as np

from src.plots import (
    save_autocorrelation_plot,
    save_autocorrelation_comparison_plot,
    save_generator_algorithm_plot,
    save_generated_density_plot,
    save_generated_sequence_plot,
    save_histogram_comparison_plot,
    save_sequence_comparison_plot,
    save_source_density_plot,
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


def test_generated_plots_are_saved(tmp_path: Path) -> None:
    from src.hyperexponential import HyperexponentialParameters

    values = np.linspace(0.1, 20.0, 300)
    parameters = HyperexponentialParameters(0.25, 12.0, 3.0)
    sequence_path = tmp_path / "generated_sequence.png"
    density_path = tmp_path / "generated_density.png"

    save_generated_sequence_plot(sequence_path, values)
    save_generated_density_plot(density_path, values, parameters)

    assert sequence_path.stat().st_size > 0
    assert density_path.stat().st_size > 0


def test_comparison_plots_are_saved(tmp_path: Path) -> None:
    from src.hyperexponential import HyperexponentialParameters

    source = np.linspace(0.1, 25.0, 300)
    generated = np.linspace(0.2, 20.0, 300)
    parameters = HyperexponentialParameters(0.25, 12.0, 3.0)
    source_density_path = tmp_path / "source_density.png"
    histogram_path = tmp_path / "histograms.png"
    sequence_path = tmp_path / "sequences.png"
    autocorrelation_path = tmp_path / "autocorrelations.png"
    source_ac = {lag: 0.01 * lag for lag in range(1, 11)}
    generated_ac = {lag: -0.005 * lag for lag in range(1, 11)}

    save_source_density_plot(source_density_path, source, parameters)
    save_histogram_comparison_plot(histogram_path, source, generated)
    save_sequence_comparison_plot(sequence_path, source, generated)
    save_autocorrelation_comparison_plot(
        autocorrelation_path,
        source_ac,
        generated_ac,
    )

    for path in (
        source_density_path,
        histogram_path,
        sequence_path,
        autocorrelation_path,
    ):
        assert path.stat().st_size > 0
