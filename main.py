import argparse
import csv
import sys
from math import sqrt
from pathlib import Path

from src.data_io import load_sequence
from src.hyperexponential import (
    empirical_moments,
    fit_hyperexponential,
    generate_hyperexponential,
    save_generated_sequence,
    theoretical_moments,
)
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
    save_stage_2_summary,
)
from src.report_tables import (
    build_form1_rows,
    save_form2,
    save_form3,
    save_generated_autocorrelations,
    save_form1,
    save_source_autocorrelations,
    save_source_histogram,
    save_stage_4_summary,
    save_stage_5_summary,
    save_stage_6_summary,
    save_stage_7_summary,
    save_final_summary,
    save_stage_3_summary,
    save_summary,
)
from src.statistics import (
    calculate_autocorrelations,
    calculate_for_sample_sizes,
    calculate_histogram,
    correlation_coefficient,
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
    parser.add_argument(
        "--seed",
        type=int,
        default=29,
        help="Seed генератора гиперэкспоненциальной последовательности.",
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

    empirical = empirical_moments(values)
    hyperexponential_parameters = fit_hyperexponential(values)
    theoretical = theoretical_moments(hyperexponential_parameters)
    stage_5_summary_path = args.out_dir / "stage_5_summary.txt"
    save_stage_5_summary(
        stage_5_summary_path,
        empirical,
        hyperexponential_parameters,
        theoretical,
    )

    generated_values = generate_hyperexponential(
        hyperexponential_parameters,
        size=len(values),
        seed=args.seed,
    )
    generated_path = args.out_dir / "generated.txt"
    generator_algorithm_path = args.out_dir / "plots" / "generator_algorithm.png"
    stage_6_summary_path = args.out_dir / "stage_6_summary.txt"
    save_generated_sequence(
        generated_path,
        generated_values,
        hyperexponential_parameters,
        args.seed,
    )
    save_generator_algorithm_plot(generator_algorithm_path)
    save_stage_6_summary(stage_6_summary_path, generated_values, args.seed)

    generated_results = calculate_for_sample_sizes(generated_values)
    form_2_path = args.out_dir / "tables" / "stage_7_form2.csv"
    generated_sequence_plot_path = args.out_dir / "plots" / "generated_sequence.png"
    generated_density_plot_path = args.out_dir / "plots" / "generated_density.png"
    generated_autocorrelation_plot_path = (
        args.out_dir / "plots" / "generated_autocorrelation.png"
    )
    generated_autocorrelation_table_path = (
        args.out_dir / "tables" / "stage_7_autocorrelation.csv"
    )
    generated_autocorrelations = calculate_autocorrelations(generated_values)
    stage_7_summary_path = args.out_dir / "stage_7_summary.txt"
    save_form2(form_2_path, generated_results, results)
    save_generated_sequence_plot(generated_sequence_plot_path, generated_values)
    save_generated_density_plot(
        generated_density_plot_path,
        generated_values,
        hyperexponential_parameters,
    )
    save_autocorrelation_plot(
        generated_autocorrelation_plot_path,
        generated_autocorrelations,
    )
    save_generated_autocorrelations(
        generated_autocorrelation_table_path,
        generated_autocorrelations,
    )
    save_stage_7_summary(
        stage_7_summary_path,
        results[300],
        generated_results[300],
        generated_autocorrelations,
        confidence_bound,
    )

    form_3_path = args.out_dir / "tables" / "form3.csv"
    source_density_path = args.out_dir / "plots" / "density_comparison.png"
    histogram_comparison_path = args.out_dir / "plots" / "histogram_comparison.png"
    sequence_comparison_path = args.out_dir / "plots" / "sequence_comparison.png"
    autocorrelation_comparison_path = (
        args.out_dir / "plots" / "autocorrelation_comparison.png"
    )
    final_summary_path = args.out_dir / "final_summary.txt"
    correlation = correlation_coefficient(values, generated_values)
    save_form3(form_3_path, autocorrelations, generated_autocorrelations)
    save_source_density_plot(
        source_density_path,
        values,
        hyperexponential_parameters,
    )
    save_histogram_comparison_plot(
        histogram_comparison_path,
        values,
        generated_values,
    )
    save_sequence_comparison_plot(
        sequence_comparison_path,
        values,
        generated_values,
    )
    save_autocorrelation_comparison_plot(
        autocorrelation_comparison_path,
        autocorrelations,
        generated_autocorrelations,
    )
    save_final_summary(
        final_summary_path,
        results[300],
        generated_results[300],
        correlation,
        args.seed,
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
    print(f"Параметры аппроксимирующего закона сохранены: {stage_5_summary_path}")
    print(f"Сгенерированная последовательность сохранена: {generated_path}")
    print(f"Алгоритм генерации сохранён: {generator_algorithm_path}")
    print(f"Итог шестого этапа сохранён: {stage_6_summary_path}")
    print(f"Форма 2 сохранена: {form_2_path}")
    print(f"График сгенерированной ЧП сохранён: {generated_sequence_plot_path}")
    print(f"Гистограмма и плотность H2 сохранены: {generated_density_plot_path}")
    print(f"Автокорреляция сгенерированной ЧП сохранена: {generated_autocorrelation_plot_path}")
    print(f"Таблица автокорреляции сгенерированной ЧП сохранена: {generated_autocorrelation_table_path}")
    print(f"Итог седьмого этапа сохранён: {stage_7_summary_path}")
    print(f"Форма 3 сохранена: {form_3_path}")
    print(f"Плотность H2 и исходная гистограмма сохранены: {source_density_path}")
    print(f"Сравнение гистограмм сохранено: {histogram_comparison_path}")
    print(f"Сравнение графиков значений сохранено: {sequence_comparison_path}")
    print(f"Сравнение автокорреляций сохранено: {autocorrelation_comparison_path}")
    print(f"Итоговое сравнение сохранено: {final_summary_path}")


if __name__ == "__main__":
    main()
