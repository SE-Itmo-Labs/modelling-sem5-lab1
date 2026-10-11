import argparse
import csv
import sys
from pathlib import Path

from src.data_io import load_sequence
from src.report_tables import build_form1_rows, save_form1, save_summary
from src.statistics import calculate_for_sample_sizes


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

    writer = csv.writer(sys.stdout, delimiter="\t")
    writer.writerows(build_form1_rows(results))
    print(f"\nТаблица сохранена: {table_path}")
    print(f"Итог для n = 300 сохранён: {summary_path}")


if __name__ == "__main__":
    main()
