from random import randrange, choice
from turtle import *
from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
food_step = 10
game_running = True

colors = ['blue', 'green', 'yellow', 'purple', 'orange']

def random_colors():
    """Regresar colores random para la serpiente y la comida."""
    food_color = choice(colors)  # Selecciona un color aleatorio para la comida
    snake_color = choice([c for c in colors if c != food_color])  # Selecciona un color diferente para la serpiente
    return snake_color, food_color

snake_color, food_color = random_colors()

def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y

def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190  # Verifica si la cabeza está dentro del área permitida

def move_food():
    """Mover comida a nueva pos."""
    new_x = randrange(-19, 19) * food_step  # Genera una nueva posición aleatoria para la comida en el eje x
    new_y = randrange(-19, 19) * food_step  # Genera una nueva posición aleatoria para la comida en el eje y

    # Asegura de que la comida no se salga de los límites
    while not inside(vector(new_x, new_y)):
        new_x = randrange(-19, 19) * food_step
        new_y = randrange(-19, 19) * food_step

    food.x = new_x
    food.y = new_y

speed = 100

def move():
    """Move snake forward one segment."""
    global snake_color, food_color, speed
    head = snake[-1].copy()
    head.move(aim)

    # Si la cabeza está fuera de los límites o colisiona con el cuerpo de la serpiente, termina el juego
    if not inside(head) or head in snake:
        game_over()
        square(head.x, head.y, 9, 'red')
        return

    snake.append(head)

    # Si la serpiente encuentra la comida
    if head == food:
        print('Snake:', len(snake))  # Imprime el tamaño de la serpiente
        move_food()
        snake_color, food_color = random_colors()  # Cambiar los colores al comer
        speed = max(10, speed * 0.9)  # Incrementar la velocidad de la serpiente al comer fruta

    else:
        snake.pop(0)

    clear()
    # Dibuja cada segmento del cuerpo de la serpiente
    for body in snake:
        square(body.x, body.y, 9, snake_color)

    # Dibuja la comida
    square(food.x, food.y, 9, food_color)
    update()

    # Utilizar la variable `speed` para controlar la velocidad del juego
    ontimer(move, int(speed))

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
    global snake, aim, food, game_running, snake_color, food_color
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    food = vector(0, 0)
    # Cada que se empiece el juego se deben de cambiar los colores de la serpiente y de la comida
    snake_color, food_color = random_colors()
    game_running = True
    move()

snake_color, food_color = random_colors()  # Asigna colores aleatorios a la serpiente y la comida
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
onkey(restart_game, 'Return')  # Reinicia el juego con Enter
move()
done()
