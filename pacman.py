"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice
from turtle import *

from freegames import floor, vector

# Estado del juego: mantiene el puntaje.
state = {'score': 0}
# Turtle para dibujar el camino y el marcador del puntaje.
path = Turtle(visible=False)
writer = Turtle(visible=False)
# Dirección inicial del pacman.
aim = vector(5, 0)
# Posición inicial de pacman.
pacman = vector(-40, -80)
# Lista de fantasmas, cada uno con una posición
#inicial y dirección de movimiento.
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# fmt: off

# se cambio el board Mariela
# Tablero de juego representado como una lista de 0s y 1s.
# 0 representa una pared, 1 representa un camino.
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # Primera fila
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,  # Segunda fila
    0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,  # Tercera fila
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,  # Cuarta fila
    0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0,  # Quinta fila
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,  # Sexta fila
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,  # Séptima fila
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,  # Octava fila
    0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0,  # Novena fila
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,  # Décima fila
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # Última fila
]

# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    # Dibuja el cuadrado.
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (point.x +  200) // 20 # Convierte coordenadas en índice x.
    y = (180 - point.y) // 20 # Convierte coordenadas en índice y.
    index = int(x + y * 20) # Calcula el índice unidimensional.
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)
    
    # Verifica si el índice está fuera de los límites o en una pared
    # (tile == 0).
    if index < 0 or index >= len(tiles):
        return False

    if tiles[index] == 0:
        return False

    # Repite la verificación con un pequeño desplazamiento para cubrir colisiones.
    index = offset(point + 19)

    if index < 0 or index >= len(tiles):
        return False

    if tiles[index] == 0:
        return False
    # Verifica si pacman está alineado con la cuadrícula
    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    bgcolor('black') # Fondo del tablero negro.
    path.color('blue') # Color de las paredes.

    for index in range(len(tiles)):
        tile = tiles[index]
        # Dibuja un cuadrado azul si el tile es mayor a 0 (camino)
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            # Dibuja un punto blanco si es un camino que no ha sido visitado
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score']) # Actualiza el puntaje en la pantalla

    clear() # Limpia los gráficos previos

    # Mueve pacman si el movimiento es válido.
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)
 
    # Verifica si pacman está en un camino y si puede comer un punto.
    if 0 <= index < len(tiles):
        if tiles[index] == 1:  # Si el valor en esa casilla es 1 (camino).
            tiles[index] = 2  # Cambia el valor a 2 (visitado).
            state['score'] += 1  # Aumenta el puntaje.
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y) # Redibuja el cuadrado como vacío.

    # Mueve a los fantasmas.
    for ghost in ghosts:
        ghost[0] += ghost[1] # Mueve al fantasma en la dirección actual
        if valid(ghost[0]):
            continue

        # Si el movimiento no es válido, cambia de dirección.
        ghost[1] = vector(-ghost[1].y, ghost[1].x)
        # Intenta moverse en la nueva dirección.
        if valid(ghost[0] + ghost[1]):
            ghost[0] += ghost[1]
            continue
        # Si no es válido, vuelve a cambiar de dirección.
        ghost[1] = vector(-ghost[1].x, -ghost[1].y)

    # Verifica si algún fantasma colisiona con pacman.
    for ghost in ghosts:
        if pacman.x < ghost[0].x < pacman.x + 20 and pacman.y < ghost[0].y < pacman.y + 20:
            writer.color('red')
            writer.write('Game Over', font=('Arial', 40, 'bold'))
            return
    
    # se aumento la velocidad de los fantasmas disminuyendo  el tiempo del temporizador. Mariela
    ontimer(move, 50)
    # Redibuja pacman y los fantasmas.
    square(pacman.x, pacman.y)

    for ghost in ghosts:
        square(ghost[0].x, ghost[0].y)

    update()
    ontimer(move, 100)  # Repite la función move cada 100 milisegundos.

def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


# Configura la ventana y el juego.
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.color('white')
writer.penup()
writer.goto(-200, 190)
writer.write(state['score'])
world()
move()
listen()
# Configura las teclas para cambiar la dirección de pacman.
onkey(lambda: change(20, 0), 'Right')
onkey(lambda: change(-20, 0), 'Left')
onkey(lambda: change(0, 20), 'Up')
onkey(lambda: change(0, -20), 'Down')
done()
