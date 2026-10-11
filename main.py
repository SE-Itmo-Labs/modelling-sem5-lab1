import argparse
import csv
import sys
from math import sqrt
from pathlib import Path

from src.data_io import load_sequence
from src.plots import (
    save_autocorrelation_plot,
    save_source_histogram_plot,
    save_source_sequence_plot,
    save_stage_2_summary,
)
from src.report_tables import (
    build_form1_rows,
    save_form1,
    save_source_autocorrelations,
    save_source_histogram,
    save_stage_4_summary,
    save_stage_3_summary,
    save_summary,
)
from src.statistics import (
    calculate_autocorrelations,
    calculate_for_sample_sizes,
    calculate_histogram,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Расчёт характеристик исходной последовательности варианта 29."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/29_data.txt"),
        help="Файл с номером варианта и 300 значениями.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("results"),
        help="Каталог для результатов.",
    )
    args = parser.parse_args()

    values = load_sequence(args.input)
    results = calculate_for_sample_sizes(values)

    table_path = args.out_dir / "tables" / "stage_1_data.csv"
    summary_path = args.out_dir / "stage_1_summary.txt"
    save_form1(table_path, results)
    save_summary(summary_path, results)

    plot_path = args.out_dir / "plots" / "source_sequence.png"
    stage_2_summary_path = args.out_dir / "stage_2_summary.txt"
    save_source_sequence_plot(plot_path, values)
    save_stage_2_summary(stage_2_summary_path, values)

    autocorrelations = calculate_autocorrelations(values)
    confidence_bound = 1.96 / sqrt(len(values))
    autocorrelation_table_path = args.out_dir / "tables" / "stage_3_autocorrelation.csv"
    autocorrelation_plot_path = args.out_dir / "plots" / "source_autocorrelation.png"
    stage_3_summary_path = args.out_dir / "stage_3_summary.txt"
    save_source_autocorrelations(autocorrelation_table_path, autocorrelations)
    save_autocorrelation_plot(
        autocorrelation_plot_path,
        autocorrelations,
    )
    save_stage_3_summary(stage_3_summary_path, autocorrelations, confidence_bound)

    histogram_boundaries, histogram_frequencies = calculate_histogram(values)
    histogram_table_path = args.out_dir / "tables" / "stage_4_histogram.csv"
    histogram_plot_path = args.out_dir / "plots" / "source_histogram.png"
    stage_4_summary_path = args.out_dir / "stage_4_summary.txt"
    save_source_histogram(
        histogram_table_path,
        histogram_boundaries,
        histogram_frequencies,
    )
    save_source_histogram_plot(histogram_plot_path, values, histogram_boundaries)
    save_stage_4_summary(
        stage_4_summary_path,
        histogram_boundaries,
        histogram_frequencies,
    )

    writer = csv.writer(sys.stdout, delimiter="\t")
    writer.writerows(build_form1_rows(results))
    print(f"\nТаблица сохранена: {table_path}")
    print(f"Итог для n = 300 сохранён: {summary_path}")
    print(f"График исходной последовательности сохранён: {plot_path}")
    print(f"Итог второго этапа сохранён: {stage_2_summary_path}")
    print(f"Автокорреляции сохранены: {autocorrelation_table_path}")
    print(f"График автокорреляции сохранён: {autocorrelation_plot_path}")
    print(f"Итог третьего этапа сохранён: {stage_3_summary_path}")
    print(f"Интервальный ряд сохранён: {histogram_table_path}")
    print(f"Гистограмма сохранена: {histogram_plot_path}")
    print(f"Итог четвёртого этапа сохранён: {stage_4_summary_path}")


if __name__ == "__main__":
    main()
