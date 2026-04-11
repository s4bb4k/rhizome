import joblib
import random
import os
from application.generators.cellular_automata import generate_map
from application.services.feature_extractor import extract_features

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(MODEL_PATH)


def generate_adaptive_map_ml(config, intentos=5):
    mejor_mapa = None
    mejor_score = -999

    for _ in range(intentos):

        config["seed"] = random.randint(0, 99999)

        mapa = generate_map(
            config["ancho"],
            config["alto"],
            config["probabilidad"],
            config["iteraciones"],
            config["seed"]
        )

        features = extract_features(mapa)
        score = model.predict([features])[0]

        if score > mejor_score:
            mejor_score = score
            mejor_mapa = mapa

        # 🔥 adaptación automática
        if score < 5:
            config["probabilidad"] -= 0.05
        elif score > 8:
            config["probabilidad"] += 0.02

        config["probabilidad"] = max(0.2, min(0.7, config["probabilidad"]))

    return {
        "map": mejor_mapa,
        "score": mejor_score,
        "config_final": config
    }