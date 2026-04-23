import random
import pandas as pd
from application.generators.cellular_automata import generate_map
from application.services.feature_extractor import extract_features
from application.services.evaluator import evaluate


def generate_dataset(n_samples=300):
    data = []

    for _ in range(n_samples):
        config = {
            "ancho": 30,
            "alto": 20,
            "probabilidad": random.uniform(0.3, 0.6),
            "iteraciones": random.randint(3, 6),
            "seed": random.randint(0, 99999)
        }

        mapa = generate_map(**config)
        features = extract_features(mapa)
        score = evaluate(features)

        data.append(features + [score])

    columns = [
        "conectividad",
        "accesibilidad",
        "enemigos",
        "monedas",
        "trampas",
        "distancia",
        "ramas",
        "score"
    ]

    return pd.DataFrame(data, columns=columns)