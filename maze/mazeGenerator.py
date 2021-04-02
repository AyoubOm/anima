"""
Maze generation using randomized DFS
Algorithm : start with a grid with walls everywhere, then do a randomized depth first search that opens the walls
"""

import pygame
import random
from PIL import Image
import shutil
from pathlib import Path


SCREEN_SIDE = 640
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = None
CELL_SIDE = None 

TMP_DIR = "./tmp_images"


def init(N):
	if SCREEN_SIDE/N <= 3:
		raise ValueError("N={} is too high".format(N))
	global screen, CELL_SIDE
	CELL_SIDE = int(SCREEN_SIDE/N)

	screen = pygame.display.set_mode((SCREEN_SIDE, SCREEN_SIDE))
	screen.fill(BLACK)
	pygame.draw.rect(screen, WHITE, (1, 1, CELL_SIDE-2, CELL_SIDE-2))

	Path(TMP_DIR).mkdir(parents=True, exist_ok=True)



def connect(x1, y1, x2, y2, images):

	# remove wall between (x1, y1) and (x2, y2)
	if y1 == y2: # vertical wall between horizontally connected cells
		wallAbscissa = max(x2, x1)
		pygame.draw.line(screen, WHITE, 
			(wallAbscissa*CELL_SIDE-1, y1*CELL_SIDE+1),
			(wallAbscissa*CELL_SIDE-1, (y1+1)*CELL_SIDE-2), width=3)

	elif x1 == x2:
		wallOrdinate = max(y1, y2)
		pygame.draw.line(screen, WHITE, 
			(x1*CELL_SIDE+1, wallOrdinate*CELL_SIDE-1),
			((x1+1)*CELL_SIDE-2, wallOrdinate*CELL_SIDE-1), width=3)

	# visit new cell
	pygame.draw.rect(screen, WHITE, (x2*CELL_SIDE+1, y2*CELL_SIDE+1, CELL_SIDE-2, CELL_SIDE-2))
	
	# display
	pygame.display.flip()

	# save image for animation
	imagePath = "{}/maze{}.png".format(TMP_DIR, len(images)+1)
	pygame.image.save(screen, imagePath)
	img = Image.open(imagePath)
	images.append(img)



def drawMaze(N):
	visited = set()
	stack = [(0, 0)]
	images = []

	while stack:
		x, y = stack[-1]

		neighbors = [(-1,0),(0,-1),(1,0),(0,1)]
		validNeighbors = []
		for nx, ny in neighbors:
			if x + nx < N and y + ny < N and x + nx >= 0 and y + ny >= 0:
				validNeighbors.append((x+nx, y+ny))

		validNeighbors = [n for n in validNeighbors if n not in visited]

		if not validNeighbors:
			stack.pop()
		else:
			nx, ny = random.choice(validNeighbors)
			connect(x, y, nx, ny, images)
			visited.add((nx, ny))
			stack.append((nx, ny))

	images[0].save('outputs/maze.gif', save_all=True, append_images=images[1:], optimize=False, loop=0)


def finish():
	shutil.rmtree(TMP_DIR)


N = 32
init(N)
drawMaze(N)


running = True
while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = False

finish()