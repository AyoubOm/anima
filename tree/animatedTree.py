"""
Python script that draws a random tree interactively using Turtle

The random properties are:
	+ The angle of the child branches given parent branch angle: Generated between [angle-MAX_DEVIATION, angle+MAX_DEVIATION]
	with a uniform distribution 
	+ The length of the child branches given parent branch length: Generated between [MIN_BRANCH_SIZE_RATIO*parent_length, MAX_BRANCH_SIZE_RATIO*parent_length]

depth is also an input parameter of the function which is the number of branch levels in the tree

You can change these values and see the effect on the generated trees.
"""


import turtle
from math import pi
from random import uniform


MAX_DEVIATION=pi/8
MAX_BRANCH_SIZE_RATIO = 0.9
MIN_BRANCH_SIZE_RATIO = 0.7

DARK_BROWN_R = 103
DARK_BROWN_G = 51
DARK_BROWN_B = 0


def tree(parent, depth, parentLength):
	if depth <= 0: return

	heading = turtle.heading()
	colorLevel = 14-depth
	color = (DARK_BROWN_R+colorLevel*9, DARK_BROWN_G+colorLevel*9, DARK_BROWN_B+colorLevel*4)

	rightAngle = uniform(0, MAX_DEVIATION*180/pi)
	rightLength = parentLength*uniform(MIN_BRANCH_SIZE_RATIO, MAX_BRANCH_SIZE_RATIO)

	turtle.pensize(depth)
	turtle.pencolor(color)
	turtle.right(rightAngle)
	turtle.forward(rightLength)

	tree(turtle.pos(), depth-1, rightLength)

	turtle.penup()
	turtle.setheading(heading)
	turtle.setpos(parent)
	turtle.pendown()

	leftAngle = uniform(0, MAX_DEVIATION*180/pi)
	leftLength = parentLength*uniform(MIN_BRANCH_SIZE_RATIO, MAX_BRANCH_SIZE_RATIO)

	turtle.pensize(depth)
	turtle.pencolor(color)
	turtle.left(leftAngle)
	turtle.forward(leftLength)

	tree(turtle.pos(), depth-1, leftLength)



def init(depth, initialLength, rootPoint):
	color = (DARK_BROWN_R, DARK_BROWN_G, DARK_BROWN_B)
	turtle.delay(0.0001)
	turtle.tracer(1500) # decrease this to see all drawing steps: 1500 takes 30s to draw the tree, default takes 3 hours
	turtle.colormode(255)
	turtle.pencolor(color)
	turtle.pensize(depth)
	turtle.penup()
	turtle.setpos(rootPoint)
	turtle.left(90)
	turtle.pendown()
	turtle.forward(initialLength)


depth = 14
initialLength = 100
init(depth, initialLength, rootPoint = (0, -200))

tree((0, -100), depth, initialLength)
turtle.done()