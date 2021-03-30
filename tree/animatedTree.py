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
from PIL import Image, EpsImagePlugin
import os
from pathlib import Path
import shutil



EpsImagePlugin.gs_windows_binary =  r'C:\Program Files (x86)\gs\gs9.53.3\bin\gswin32c'


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





TMP_DIR = "./tmp_images/"
Path(TMP_DIR).mkdir(parents=True, exist_ok=True)



def draw():
	depth = 14
	initialLength = 100
	init(depth, initialLength, rootPoint = (0, -260))

	tree((0, -160), depth, initialLength)
	turtle.done()

	turtle.ontimer(stop, 500)


running = True
FRAMES_PER_SECOND = 100

def stop():
	running = False

images = []



def addToGif(canvas, counter):
	"""
	The gif is created using captures of drawing state
	"""
	fileName = TMP_DIR+"out_tree{0:03d}".format(counter[0])
	canvas.postscript(file = fileName + '.eps')
	img = Image.open(fileName + '.eps')
	img.save(fileName + '.png', 'png') # appending image from ".eps" directly doesn't work
	img = Image.open(fileName + '.png')
	images.append(img)




def save(counter=[1]):
	addToGif(turtle.getcanvas(), counter)
	counter[0] += 1
	if running:
		turtle.ontimer(save, int(1000 / FRAMES_PER_SECOND))

# shutil.rmtree(TMP_DIR)

save()  # start the recording

turtle.ontimer(draw, 500)

turtle.done()

images[0].save('out.gif', save_all=True, append_images=images[1:], optimize=False, loop=0)
