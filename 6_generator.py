import numpy as np

from lab_common import RESULTS_DIR, SEED, fit_h2, generate_values, load_values


def run() -> None:

    parameters = fit_h2(load_values()) # парсим параметры

    values = generate_values(parameters) # генерим значения

    RESULTS_DIR.mkdir(parents=True, exist_ok=True) # сохраняем в папку

    header = f"seed={SEED}; q={parameters.q:.6f}; t1={parameters.t1:.6f}; t2={parameters.t2:.6f}"

    np.savetxt(RESULTS_DIR / "generated.txt", values, fmt="%.10f", header=header) # сохраняем в папку

    print(f"6. Сгенерировано {len(values)} значений с seed = {SEED}.")


if __name__ == "__main__":
    run()
