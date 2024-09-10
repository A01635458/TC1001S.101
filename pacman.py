from random import choice, randint
from turtle import *
from freegames import floor, vector

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

def generate_grid(width, height):
    "Genera un grid aleatorio de tamaño width x height con paredes y caminos."
    grid = [0] * (width * height)
    
    # Llena el borde con paredes
    for x in range(width):
        grid[x] = 0  # Pared superior
        grid[(height - 1) * width + x] = 0  # Pared inferior
    for y in range(height):
        grid[y * width] = 0  # Pared izquierda
        grid[y * width + (width - 1)] = 0  # Pared derecha
    
    # Llena el resto del grid aleatoriamente
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if randint(0, 1) == 1:
                grid[i * width + j] = 1  # Camino
            else:
                grid[i * width + j] = 0  # Pared

    return grid

# Genera un grid aleatorio de 20x20
tiles = generate_grid(20, 20)

# Funcion para dibujar un cuadrado usando x, y
def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    "Return offset of point in tiles."
    # Calcula la posición en x dentro de la cuadrícula, ajustando la coordenada a la grilla de 20x20.
    x = (floor(point.x, 20) + 200) / 20

    # Calcula la posición en y dentro de la cuadrícula, ajustando la coordenada a la grilla de 20x20.
    y = (180 - floor(point.y, 20)) / 20
    
    # Calcula el índice en la lista 'tiles' usando las coordenadas de x e y.
    index = int(x + y * 20)
    return index

def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)
     # Verifica si el valor del tile en ese índice es una pared (0).
    if tiles[index] == 0:
        return False
    #Verifica el índice del punto + 19 para asegurarse de que no sea una pared.
    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    "Draw world using path."
    bgcolor('black')
    path.color('blue')
    # Recorre cada índice en la lista 'tiles', que representa la cuadrícula del mundo.
    for index in range(len(tiles)):
        tile = tiles[index]
        # Si el valor del tile es mayor que 0, es decir, es un camino o un punto.
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            # Si el tile tiene un valor de 1 (indicando un camino con puntos).
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def pursue(ghost):
    "Mueve el fantasma hacia Pacman."
    ghost_position, ghost_course = ghost

    # Definir las posibles direcciones de movimiento
    directions = [
        vector(0, 5),    # Arriba
        vector(0, -5),   # Abajo
        vector(5, 0),    # Derecha
        vector(-5, 0),   # Izquierda
    ]

    # Evitar la reversa inmediata
    opposite = vector(-ghost_course.x, -ghost_course.y)
    possible_directions = [d for d in directions if d != opposite]

    # Filtrar las direcciones válidas
    valid_directions = [d for d in possible_directions if valid(ghost_position + d)]

    # Si no hay direcciones válidas (fantasma está atrapado), permitir reversa
    if not valid_directions:
        valid_directions = [d for d in directions if valid(ghost_position + d)]

    # Si aún no hay direcciones válidas, el fantasma no se mueve
    if not valid_directions:
        return

    # Elegir la dirección que minimiza la distancia a Pacman
    min_distance = float('inf')
    best_direction = ghost_course  # Dirección por defecto

    for d in valid_directions:
        new_position = ghost_position + d
        distance = (pacman.x - new_position.x)**2 + (pacman.y - new_position.y)**2
        if distance < min_distance:
            min_distance = distance
            best_direction = d

    # Actualizar la dirección del fantasma
    ghost_course.x = best_direction.x
    ghost_course.y = best_direction.y

# La función `move` mueve a Pacman y los fantasmas, actualiza la puntuación y el tablero,
# y verifica si hay colisión con un fantasma. Repite el proceso cada 100 ms.
def move():
    "Mueve a Pacman y todos los fantasmas."
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for ghost in ghosts:
        pursue(ghost)
        ghost_position, ghost_course = ghost
        if valid(ghost_position + ghost_course):
            ghost_position.move(ghost_course)

        up()
        goto(ghost_position.x + 10, ghost_position.y + 10)
        dot(20, 'red')

    update()

    for ghost in ghosts:
        ghost_position, _ = ghost
        if abs(pacman - ghost_position) < 20:
            writer.goto(0, 0)
            writer.color('red')
            writer.write("¡Game Over!", align="center", font=("Arial", 16, "normal"))
            return

    ontimer(move, 100)

def change(x, y):
    "Cambia la dirección de Pacman si es válida."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
