"""
Step 1) Create two paddles A and B on the left and right sides of the screen.
Step 2) Create a ball.
Step 3) Create an event to move the paddle vertically by pressing a certain key.
Step 4) Create the function to update the score after each player misses a collision.

source: https://codinghero.ai/5-interesting-games-in-python-that-kids-can-make/
"""

# Import required library
import turtle

# Create screen
sc = turtle.Screen()
sc.title("Francesco game")
# sc.bgcolor("white")
sc.setup(width=1000, height=600)
# sc.screensize(canvwidth=1000, canvheight=600, bg="white")
sc.bgpic("ping_pong_table.PNG")

# Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape('circle')
left_pad.color("blue")  #  was: right_pad.color("black")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-400, 0)

# Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("circle",)
right_pad.color("red")  #  was: right_pad.color("black")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400, 0)

# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(49)
hit_ball.shape('turtle') # was: hit_ball.shape("circle")

hit_ball.color("black")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5

# Initialize the score
left_player = 0
right_player = 0

# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left_player : 0 Right_player: 0",
             align="center", font=("Courier", 24, "normal"))


# Functions to move paddle vertically
def paddleaup():
    y = left_pad.ycor()
    y += 25
    left_pad.sety(y)


def paddleadown():
    y = left_pad.ycor()
    y -= 25
    left_pad.sety(y)


def paddlebup():
    y = right_pad.ycor()
    y += 25
    right_pad.sety(y)


def paddlebdown():
    y = right_pad.ycor()
    y -=25
    right_pad.sety(y)


# Keyboard bindings
sc.listen()
sc.onkeypress(paddleaup, "w")
sc.onkeypress(paddleadown, "s")
sc.onkeypress(paddlebup, "Up")
sc.onkeypress(paddlebdown, "Down")

while max(right_player, left_player) < 25:
    # turtle.circle(40)
    # turtle.right(36)
    sc.update()

    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    # Checking borders
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1

    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        left_player += 1
        sketch.clear()
        sketch.write("Left_player : {} Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        right_player += 1
        sketch.clear()
        sketch.write("Left_player : {} Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    # Paddle ball collision
    if (hit_ball.xcor() > 360 and
        hit_ball.xcor() < 370) and (hit_ball.ycor() < right_pad.ycor() + 40 and hit_ball.ycor() > right_pad.ycor() - 40):
        hit_ball.setx(360)
        hit_ball.dx *= -1

    if (hit_ball.xcor() < -360 and
        hit_ball.xcor() > -370) and (hit_ball.ycor() < left_pad.ycor() + 40 and hit_ball.ycor() > left_pad.ycor() - 40):
        hit_ball.setx(-360)
        hit_ball.dx *= -1