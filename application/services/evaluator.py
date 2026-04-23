def evaluate(features):
    conectividad, accesibilidad, enemigos, monedas, trampas, distancia, ramas = features

    score = (
        (conectividad * 5)
        + (accesibilidad * 2)
        + (monedas * 0.5)
        - (trampas * 0.7)
    )

    return score