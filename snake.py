"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to mouse clicks.
"""

from random import randrange
from turtle import *

from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
#luisa, paso del movimiento
food_step = 10
#volver a empezar con enter despues de morir, luisa
game_running = True


def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y


def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

#mover comida a nueva pos, Luisa
def move_food():
    """Move food to a new position."""
    new_x = randrange(-19, 19) * food_step
    new_y = randrange(-19, 19) * food_step

    # Asegúrate de que la comida no se salga de los límites
    while not inside(vector(new_x, new_y)):
        new_x = randrange(-19, 19) * food_step
        new_y = randrange(-19, 19) * food_step

    food.x = new_x
    food.y = new_y


def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        game_over()
        square(head.x, head.y, 9, 'red')
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        #llamar, Luisa
        move_food()
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, 100)

#funciones para el enter y volver a iniciar, luisa
def game_over():
    """Handle game over state."""
    global game_running
    game_running = False
    clear()
    penup()
    goto(0, 0)
    color('red')
    write("Game Over! Press Enter to Restart", align="center", font=("Arial", 16, "bold"))
    update()

def restart_game():
    """Restart the game."""
    global snake, aim, food, game_running
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    food = vector(0, 0)
    game_running = True
    move()

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
onkey(restart_game, 'Return') #luisa
move()
done()
