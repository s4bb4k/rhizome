import os
import joblib
import random

from application.generators.cellular_automata import generate_map
from application.services.feature_extractor import extract_features
from application.services.evaluation_metrics import evaluar_mapa


# =========================
# 📦 CARGAR MODELO
# =========================
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(MODEL_PATH)


# =========================
# 🎯 ADAPTACIÓN POR USUARIO
# =========================
def adapt_with_user(config, user_profile, user_behavior, context):

    prob = config.get("probabilidad", 0.45)

    # 🎮 NIVEL
    nivel = user_profile.get("nivel", "intermedio")
    if nivel == "novato":
        prob -= 0.05
    elif nivel == "experto":
        prob += 0.05

    # ⚔️ PREFERENCIA
    preferencia = user_profile.get("preferencia", "balanceado")
    if preferencia == "exploracion":
        prob -= 0.03
    elif preferencia == "combate":
        prob += 0.03

    # 📊 COMPORTAMIENTO
    muertes = user_behavior.get("muertes", 0)
    if muertes > 5:
        prob -= 0.03

    # 🌍 CONTEXTO
    dificultad = context.get("dificultad", "media")
    if dificultad == "facil":
        prob -= 0.05
    elif dificultad == "dificil":
        prob += 0.05

    # 🔒 CONTROL DE RANGO (EVITA MAPAS VACÍOS)
    prob = max(0.4, min(0.65, prob))

    config["probabilidad"] = prob

    return config


# =========================
# 🧠 GENERADOR ADAPTATIVO ML
# =========================
def generate_adaptive_map_ml(config, user_profile, user_behavior, context, intentos=5):

    # adaptar config
    config = adapt_with_user(config, user_profile, user_behavior, context)

    mejor_mapa = None
    mejor_score = -999
    mejor_metricas = None

    # 🔍 DEBUG (puedes comentar luego)
    print("Probabilidad final usada:", config["probabilidad"])

    for _ in range(intentos):

        # generar seed aleatorio
        config["seed"] = random.randint(0, 99999)

        mapa = generate_map(
            config["ancho"],
            config["alto"],
            config["probabilidad"],
            config["iteraciones"],
            config.get("seed")
        )

        # extraer features
        features = extract_features(mapa)

        # predicción ML
        score = model.predict([features])[0]

        # evaluar métricas reales
        metricas = evaluar_mapa(mapa)

        # 🔥 FILTRO ANTI-MAPA VACÍO
        accesibilidad = metricas.get("accesibilidad", 0)

        if accesibilidad > 0.95:
            continue  # descarta mapas vacíos

        # seleccionar mejor mapa
        if score > mejor_score:
            mejor_score = score
            mejor_mapa = mapa
            mejor_metricas = metricas

    # ⚠️ fallback si todos fueron descartados
    if mejor_mapa is None:
        mapa = generate_map(
            config["ancho"],
            config["alto"],
            0.5,  # valor seguro
            config["iteraciones"],
            random.randint(0, 99999)
        )

        mejor_mapa = mapa
        mejor_metricas = evaluar_mapa(mapa)
        mejor_score = model.predict([extract_features(mapa)])[0]

    return {
        "map": mejor_mapa,
        "score": mejor_score,
        "metricas": mejor_metricas,
        "config_final": config
    }