import turtle
import random

wn = turtle.Screen()
wn.title("circle")
#wn.tracer(0)


cir = turtle.Turtle()
cir.shape("square")
cir.speed(0)


for i in range(72): # choose identity from 1 to 72
	colors = ("black red blue brown purple pink green magenta coral").split()
	cir.color(random.choice(colors))
	cir.circle(100) # turtule's circle size'
	cir.left(5) # turtule will rotate at angle 5

cir.hideturtle() # hide turtle

wn.mainloop()