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
from PIL import Image
from freegames import path

#car = path('car.gif')
letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:8]  
tiles = letters * 2
shuffle(tiles)
state = {'mark': None}
hide = [True] * 16
tap_count = 0 

# Dibujar el cuadrado del grid
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
    return int((x + 200) // 50  + ((y + 200) // 50) * 4)


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 4) * 50  - 200, (count // 4) * 50 - 200


def tap(x, y):
    """Update mark and hidden tiles based on tap."""
    global tap_count   
    spot = index(x, y)
    mark = state['mark']
    tap_count += 1

    # Verifica que el índice esté dentro del rango permitido
    if 0 <= spot < len(tiles):
        # Si no hay ningún tile marcado, o el tile marcado es el mismo que el clicado,
        # o los tiles no coinciden
        if mark is None or mark == spot or tiles[mark] != tiles[spot]:
            state['mark'] = spot
        else:
            # Si los tiles coinciden, desoculta ambos tiles
            hide[spot] = False
            hide[mark] = False
            state['mark'] = None


def draw():
    """Draw image and tiles."""
    clear() # Limpia la pantalla para redibujar todo
    
    #luisa
    up()
    goto(-180, 180)
    color('black')
    write(f'Taps: {tap_count}', font=('Arial', 16, 'normal'))

    for count in range(16):
        # Si el tile está oculto
        if hide[count]:
            # Obtiene las coordenadas del tile
            x, y = xy(count)
            square(x, y) # Dibuja el tile en la pantalla

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



setup(420, 420, 370, 0)
#addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
