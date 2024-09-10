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
# fmt: off

# se cambio el board Mariela
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

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (point.x +  200) // 20
    y = (180 - point.y) // 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)
    
    if index < 0 or index >= len(tiles):
        return False

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if index < 0 or index >= len(tiles):
        return False

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if 0 <= index < len(tiles):
        if tiles[index] == 1:  # Si el valor en esa casilla es 1 (camino).
            tiles[index] = 2  # Cambia el valor a 2 (visitado).
            state['score'] += 1  # Aumenta el puntaje.
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y) 

    for ghost in ghosts:
        ghost[0] += ghost[1]
        if valid(ghost[0]):
            continue

        ghost[1] = vector(-ghost[1].y, ghost[1].x)

        if valid(ghost[0] + ghost[1]):
            ghost[0] += ghost[1]
            continue

        ghost[1] = vector(-ghost[1].x, -ghost[1].y)

        if valid(ghost[0] + ghost[1]):
            ghost[0] += ghost[1]
            continue

        ghost[1] = vector(-ghost[1].x, -ghost[1].y)

    for ghost in ghosts:
        if pacman.x < ghost[0].x < pacman.x + 20 and pacman.y < ghost[0].y < pacman.y + 20:
            writer.color('red')
            writer.write('Game Over', font=('Arial', 40, 'bold'))
            return
    
    # se aumento la velocidad de los fantasmas disminuyendo  el tiempo del temporizador. Mariela
    ontimer(move, 50)

    square(pacman.x, pacman.y)

    for ghost in ghosts:
        square(ghost[0].x, ghost[0].y)

    update()
    ontimer(move, 100)

def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

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
onkey(lambda: change(20, 0), 'Right')
onkey(lambda: change(-20, 0), 'Left')
onkey(lambda: change(0, 20), 'Up')
onkey(lambda: change(0, -20), 'Down')
done()
