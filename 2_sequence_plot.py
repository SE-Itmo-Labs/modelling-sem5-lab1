import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lab_common import PLOTS_DIR, load_values


def run() -> None:
    values = load_values()
    numbers = np.arange(1, len(values) + 1)

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 4.8))

    axis.plot(
        numbers,
        values,
        color="#2563a6",
        linewidth=1.0,
        label="Исходная последовательность",
    )

    axis.set(xlabel="Номер значения", ylabel="Значение", xlim=(1, len(values)))
    axis.set_ylim(bottom=0)
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper left")

    figure.tight_layout()
    figure.savefig(PLOTS_DIR / "source_sequence.png", dpi=220, bbox_inches="tight")
    
    plt.close(figure)
    print("2. График исходной последовательности сохранён.")


if __name__ == "__main__":
    run()
