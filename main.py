from importlib import import_module


SCRIPTS = (
    "1_statistics",
    "2_sequence_plot",
    "3_autocorrelation",
    "4_histogram",
    "5_distribution",
    "6_generator",
    "7_generated_analysis",
    "8_comparison",
)


def main() -> None:
    for script in SCRIPTS:
        import_module(script).run()


if __name__ == "__main__":
    main()
