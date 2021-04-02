"""
Maze generation using randomized DFS
Algorithm : start with a grid with walls everywhere, then do a randomized depth first search that opens the walls
"""

import pygame
import random

SCREEN_SIDE = 640
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = None
CELL_SIDE = None 



def initGrid(N):
	if SCREEN_SIDE/N <= 3:
		raise ValueError("N={} is too high".format(N))
	global screen, CELL_SIDE
	screen = pygame.display.set_mode((SCREEN_SIDE, SCREEN_SIDE))
	CELL_SIDE = int(SCREEN_SIDE/N)
	screen.fill(BLACK)
	pygame.draw.rect(screen, WHITE, (1, 1, CELL_SIDE-2, CELL_SIDE-2))



def connect(x1, y1, x2, y2):
	"""
	removes the wall between two cells and visit the new cell
	"""

	# remove wall
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

	pygame.display.flip()




def drawMaze(N):
	visited = set()
	stack = [(0, 0)]

	while stack:
		x, y = stack[-1]

		neighbors = [(-1,0),(0,-1),(1,0),(0,1)]
		validNeighbors = []
		for nx,ny in neighbors:
			if x + nx < N and y + ny < N and x + nx >= 0 and y + ny >= 0:
				validNeighbors.append((x+nx, y+ny))


		validNeighbors = [n for n in validNeighbors if n not in visited]

		if not validNeighbors:
			stack.pop()

		else:
			nx, ny = random.choice(validNeighbors)
			connect(x, y, nx, ny)
			visited.add((nx, ny))
			stack.append((nx, ny))



N = 32
initGrid(N)
drawMaze(N)



r²ning = True
while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = False

