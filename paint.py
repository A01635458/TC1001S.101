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

def line(start, end):
    """Draw line from start to end."""
    up()
    goto(start.x, start.y)
    down()
    goto(end.x, end.y)


def square(start, end):
    """Draw square from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(4):
        forward(end.x - start.x)
        left(90)

    end_fill()


def draw_circle(start, end):
    """Draw circle from start to end."""
    #codigo modificado usando nano por Luisa
    up()
    goto(start.x, start.y)
    down()
    begin_fill()
    radius = ((end.x - start.x)**2 + (end.y - start.y)**2) ** 0.5
    circle(radius)
    end_fill()
	


def rectangle(start, end):
    """Draw rectangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    width = end.x - start.x
    height = end.y - start.y
    begin_fill()
    for _ in range(2):
      forward(width)
      left(90)
      forward(height)
      left(90)
    end_fill()




def triangle(start, end):
    """Draw triangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    # Draw the first side of the triangle
    goto(end.x, end.y)
    
    # Calculate the third point of the triangle
    dx = end.x - start.x
    dy = end.y - start.y
    length = ((dx**2) + (dy**2)) ** 0.5
    
    # Find a point at 60 degrees to form an equilateral triangle
    third_point_x = start.x - dy
    third_point_y = start.y + dx
    
    goto(third_point_x, third_point_y)
    goto(start.x, start.y)

    end_fill()
    
  
def tap(x, y):
    """Store starting point or draw shape."""
    start = state['start']

    if start is None:
        state['start'] = vector(x, y)
    else:
        shape = state['shape']
        end = vector(x, y)
        shape(start, end)
        state['start'] = None


def store(key, value):
    """Store value in state at key."""
    state[key] = value


state = {'start': None, 'shape': line}
setup(420, 420, 370, 0)
onscreenclick(tap)
listen()
onkey(undo, 'u')
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'R')
#color agregado por Luisa usando nano
onkey(lambda: color('yellow'),'Y')
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', draw_circle), 'c')
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')
done()
