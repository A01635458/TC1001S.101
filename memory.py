"""Memory, puzzle game of number pairs.

Exercises:

1. Count and print how many taps occur.
2. Decrease the number of tiles to a 4x4 grid.
3. Detect when all tiles are revealed.
4. Center single-digit tile.
5. Use letters instead of tiles.
"""

from random import *
from turtle import *

from freegames import path

car = path('car.gif')
letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:16]  
tiles = letters * 2
state = {'mark': None}
hide = [True] * 32
tap_count = 0 

def square(x, y):
    """Draw white square with black outline at (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Convert (x, y) coordinates to tiles index."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 4)


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 8) * 50 - 200, (count // 4) * 50 - 200


def tap(x, y):
    """Update mark and hidden tiles based on tap."""
    global tap_count   
    spot = index(x, y)
    mark = state['mark']
    tap_count += 1

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None


def draw():
    """Draw image and tiles."""
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    #luisa
    up()
    goto(-180, 180)
    color('black')
    write(f'Taps: {tap_count}', font=('Arial', 16, 'normal'))

    for count in range(32):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 25, y + 8)  # Ajuste para centrar el dígito Mariela
        color('black')
        write(tiles[mark], align='center', font=('Arial', 30, 'normal'))

    #luisa
    if all(not hidden for hidden in hide):
        up()
        goto(0, 0)
        color('green')
        write("¡Juego completado!", align="center", font=('Arial', 30, 'normal'))
    update()
    ontimer(draw, 100)


shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
