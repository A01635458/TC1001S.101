"""Cannon, hitting targets with projectiles.

Exercises

1. Keep score by counting target hits.
2. Vary the effect of gravity.
3. Apply gravity to the targets.
4. Change the speed of the ball.
"""

from random import randrange
from turtle import *
from freegames import vector

# Inicializa las posiciones de la bola y los objetivos.
ball = vector(-200, -200)  # La bola comienza fuera de la pantalla
speed = vector(0, 0)  # Velocidad inicial de la bola
targets = []  # Lista para almacenar los objetos

def tap(x, y):
    """Respond to screen tap."""
    # Responde a un toque en la pantalla, lanzando la bola desde su posición inicial
    if not inside(ball):
        # Asegúrate de que la bola no esté en movimiento cuando se reposicione
        ball.x = -199
        ball.y = -199
        # Cambia las velocidades para que la bola vaya más rápido en función de la posición del tap
        speed.x = (x + 200) / 10
        speed.y = (y + 200) / 10

def inside(xy):
    """Return True if xy within screen."""
    # Comprueba si el objeto (bola o objetivo) está dentro de los límites de la pantalla
    return -200 < xy.x < 200 and -200 < xy.y < 200

def draw():
    """Draw ball and targets."""
    # Dibuja la bola y los objetivos en la pantalla
    clear()  # Limpia la pantalla
    # Dibuja cada objetivo como un punto azul
    for target in targets:
        goto(target.x, target.y)
        dot(20, 'blue')

    # Dibuja la bola si está dentro de los límites de la pantalla
    if inside(ball):
        goto(ball.x, ball.y)
        dot(6, 'red')

    update()

def move():
    """Move ball and targets."""
    # Genera aleatoriamente un nuevo objetivo cada 40 ciclos
    if randrange(40) == 0:
        y = randrange(-150, 150)  # Posición aleatoria vertical del nuevo objetivo
        target = vector(200, y)  # El nuevo objetivo aparece en el borde derecho
        targets.append(target)  # Añade el nuevo objetivo a la lista

    # Mueve todos los objetivos hacia la izquierda
    for target in targets:
        target.x -= 1.5
        # Reposicionar el objetivo si sale de la pantalla
        if not inside(target):
            target.x = 200
            target.y = randrange(-150, 150)

    # Si la bola está dentro de los límites, le aplica gravedad
    if inside(ball):
        speed.y -= 0.35  # Aplicar gravedad a la bola
        ball.move(speed)
        # Reposicionar la bola cuando sale de la ventana
        if not inside(ball):
            ball.x = -200
            ball.y = randrange(-150, 150)
            speed.x = (randrange(-200, 200)) / 10
            speed.y = (randrange(-200, 200)) / 10
    else:
        # Asegurarse de que la bola tenga velocidad positiva al reposicionarse
        ball.x = -200
        ball.y = randrange(-150, 150)
        speed.x = (randrange(-200, 200)) / 10
        speed.y = (randrange(-200, 200)) / 10

    dupe = targets.copy()  # Copia de los objetivos actuales
    targets.clear()  # Limpia la lista de objetivos

    for target in dupe:
        if abs(target - ball) > 13:  # Si la distancia entre la bola y el objetivo es mayor a 13, no hay colisión
            targets.append(target)  # Vuelve a añadir el objetivo a la lista

    draw()  # Dibuja los objetos actualizados en la pantalla

    ontimer(move, 25)

setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
onscreenclick(tap)  # Asigna la función tap al evento de clic en la pantalla
move()
done()
