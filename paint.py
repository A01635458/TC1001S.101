"""Paint, for drawing shapes.

Exercises

1. Add a color.
2. Complete circle.
3. Complete rectangle.
4. Complete triangle.
5. Add width parameter.
"""

from turtle import *

from freegames import vector
import math

# Funcion para dibujar lineas
def line(start, end):
    """Draw line from start to end."""
    up()  # Levanta el lápiz para mover sin dibujar
    goto(start.x, start.y) # Mueve el cursor a la posición de inicio
    down() # Baja el lápiz para empezar a dibuja
    goto(end.x, end.y) # Dibuja una línea hasta la posición final


# Funcion para dibujar cuadrados
def square(start, end):
    """Draw square from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill() # Llena el área del cuadrado con color
    
    # Dibuja los cuatro lados del cuadrado
    for count in range(4): 
        forward(end.x - start.x)
        left(90) # Gira 90 grados a la izquierda para formar un ángulo recto

    end_fill()

# Funcion para dibujar circulos
def draw_circle(start, end):
    """Draw circle from start to end."""
    #codigo modificado usando nano por Luisa
    up()
    goto(start.x, start.y)
    down()
    begin_fill()
    radius = ((end.x - start.x)**2 + (end.y - start.y)**2) ** 0.5 # Calcula el radio del círculo
    circle(radius) # Dibuja el círculo con el radio calculado
    end_fill()
	
# Funcion para dibujar rectangulos
def rectangle(start, end):
    """Draw rectangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    width = end.x - start.x # Calcula el ancho del rectángulo
    height = end.y - start.y # Calcula la altura del rectángulo
    begin_fill()

    # Dibuja dos pares de lados del rectángulo
    for _ in range(2):
      forward(width) # Dibuja el ancho del rectángulo
      left(90)
      forward(height) # Dibuja el largo del rectángulo
      left(90)
    end_fill()

# Funcion para dibujar triangulos
def triangle(start, end):
    """Draw triangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    # Dibuja el primer lado del triángulo
    goto(end.x, end.y)
    
    # Calcula el tercer punto del triángulo
    dx = end.x - start.x
    dy = end.y - start.y
    length = ((dx**2) + (dy**2)) ** 0.5
    
     # Encuentra un punto a 60 grados para formar un triángulo equilátero
    third_point_x = start.x - dy # Calcula la coordenada x del tercer punto
    third_point_y = start.y + dx # Calcula la coordenada y  del tercer punto
    
    goto(third_point_x, third_point_y)
    goto(start.x, start.y)  Regresa al punto de inicio para cerrar el triángulo

    end_fill()
    
  
def tap(x, y):
    """Store starting point or draw shape."""
    start = state['start']

    if start is None:
        state['start'] = vector(x, y)
    else:
        shape = state['shape']  # Obtiene la función de forma seleccionada desde el estado
        end = vector(x, y)
        shape(start, end) # Dibuja la forma desde el inicio hasta el final
        state['start'] = None # Restablece el punto de inicio para la siguiente forma


def store(key, value):
    """Store value in state at key."""
    state[key] = value 

#  Diccionario para almacenar el estado actual del punto de inicio y la forma seleccionada 
state = {'start': None, 'shape': line}
setup(420, 420, 370, 0)
onscreenclick(tap)
listen()
onkey(undo, 'u')

# Asocia diferentes teclas con funciones específicas para cambiar el color de dibujo
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'R')
#color agregado por Luisa usando nano
onkey(lambda: color('yellow'),'Y')

# Asocia teclas para cambiar la forma de dibujo
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', draw_circle), 'c')
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')
done()
