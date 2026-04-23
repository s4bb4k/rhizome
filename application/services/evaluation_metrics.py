from application.services.feature_extractor import extract_features


def evaluar_mapa(mapa):
    """
    Evalúa un mapa en términos de:
    - calidad
    - coherencia
    - eficiencia
    """

    features = extract_features(mapa)

    conectividad = features[0]
    accesibilidad = features[1]
    enemigos = features[2]
    monedas = features[3]
    trampas = features[4]

    # MÉTRICAS

    # Calidad: mezcla de accesibilidad y contenido
    calidad = (accesibilidad * 0.6) + (conectividad * 0.4)

    # Coherencia: estructura lógica del mapa
    coherencia = conectividad

    # Eficiencia: uso del espacio
    eficiencia = accesibilidad

    return {
        "calidad": round(calidad, 3),
        "coherencia": round(coherencia, 3),
        "eficiencia": round(eficiencia, 3),
        "detalle": {
            "enemigos": enemigos,
            "monedas": monedas,
            "trampas": trampas
        }
    }