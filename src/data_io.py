from pathlib import Path

import numpy as np


EXPECTED_VALUES_COUNT = 300


def load_sequence(path: str | Path, expected_variant: int = 29) -> np.ndarray:
    tokens = Path(path).read_text(encoding="utf-8-sig").split()
    if not tokens:
        raise ValueError("Файл с исходными данными пуст.")

    variant = int(tokens[0])
    if variant != expected_variant:
        raise ValueError(
            f"Ожидался вариант {expected_variant}, в файле указан вариант {variant}."
        )

    values = np.array([float(token.replace(",", ".")) for token in tokens[1:]])
    if len(values) != EXPECTED_VALUES_COUNT:
        raise ValueError(
            f"Ожидалось {EXPECTED_VALUES_COUNT} значений, получено {len(values)}."
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("Последовательность содержит бесконечность или NaN.")
    if np.any(values < 0):
        raise ValueError("Последовательность содержит отрицательные значения.")

    return values
