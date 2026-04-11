import random

def generate_map(ancho, alto, probabilidad, iteraciones, seed=None):
    if seed is not None:
        random.seed(seed)

    grid = [
        [1 if random.random() < probabilidad else 0 for _ in range(ancho)]
        for _ in range(alto)
    ]

    for _ in range(iteraciones):
        new_grid = []
        for y in range(alto):
            row = []
            for x in range(ancho):
                vecinos = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < alto and 0 <= nx < ancho:
                            vecinos += grid[ny][nx]
                row.append(1 if vecinos > 4 else 0)
            new_grid.append(row)
        grid = new_grid

    return grid