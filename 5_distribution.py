from lab_common import empirical_moments, fit_h2, load_values, theoretical_moments


def run() -> None:
    values = load_values()
    empirical = empirical_moments(values)
    parameters = fit_h2(values)
    theoretical = theoretical_moments(parameters)
    print("5. Параметры гиперэкспоненциального распределения H2")
    print(f"q = {parameters.q:.6f}")
    print(f"t1 = {parameters.t1:.6f}")
    print(f"t2 = {parameters.t2:.6f}")
    print(f"Эмпирическое среднее: {empirical['mean']:.6f}")
    print(f"Теоретическое среднее: {theoretical['mean']:.6f}")
    print(f"Эмпирический второй момент: {empirical['second_moment']:.6f}")
    print(f"Теоретический второй момент: {theoretical['second_moment']:.6f}")


if __name__ == "__main__":
    run()
