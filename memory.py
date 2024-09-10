from random import shuffle
from turtle import *

from freegames import path

# Cargar la imagen del coche
car = path('car.gif')

# Inicializar los azulejos (tiles) con números del 0 al 31, duplicados
tiles = list(range(32)) * 2

# Estado del juego con un marcador (mark) para la posición del primer azulejo tocado
state = {'mark': None}

# Lista para controlar la visibilidad de cada azulejo; True significa oculto
hide = [True] * 64

# Contador para el número de toques realizados
tap_count = 0

# Variable para controlar si el juego ha terminado
game_over = False

def square(x, y):
    """Dibuja un cuadrado blanco con borde negro en las coordenadas (x, y)."""
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
    """Convierte las coordenadas (x, y) a un índice de azulejo."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)

def xy(count):
    """Convierte el número de azulejo a coordenadas (x, y)."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200

def tap(x, y):
    """Actualiza el marcador y la visibilidad de los azulejos basándose en el toque."""
    global tap_count, game_over  # Acceder al contador de toques y al estado del juego
    if game_over:
        return

    spot = index(x, y)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None

    tap_count += 1  # Incrementar el contador de toques
    print(f"Number of taps: {tap_count}")  # Mostrar el número de toques

    # Verificar si todos los azulejos están revelados
    if all(not h for h in hide):
        print("All tiles are revealed!")
        game_over = True  # Cambiar el estado del juego a terminado
        return  # No hacer más actualizaciones

def draw():
    """Dibuja la imagen y los azulejos."""
    if game_over:
        return  # No dibujar si el juego ha terminado

    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 15, y + 10)  # Ajustar para centrar el dígito en el cuadro
        color('black')
        # Escribir la letra en lugar del número
        write(chr(65 + tiles[mark]), font=('Arial', 30, 'normal'))

    update()
    ontimer(draw, 100)

# Mezclar los azulejos
shuffle(tiles)

# Configuración de la ventana
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
