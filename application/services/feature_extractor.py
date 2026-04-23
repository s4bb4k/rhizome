def extract_features(grid):
    alto = len(grid)
    ancho = len(grid[0])

    total = alto * ancho
    libres = sum(cell == 0 for row in grid for cell in row)

    accesibilidad = libres / total
    conectividad = 1 if libres > 0 else 0

    enemigos = libres // 20
    monedas = libres // 15
    trampas = (total - libres) // 25

    distancia = 5
    ramificaciones = 2

    return [
        conectividad,
        accesibilidad,
        enemigos,
        monedas,
        trampas,
        distancia,
        ramificaciones
    ]