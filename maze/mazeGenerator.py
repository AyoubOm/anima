import pygame
import random

SCREEN_SIDE = 640
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = None
UNIT_SIDE = None 



# pygame.draw.line(screen, (0, 0, 255), (0, 0), (639, 479))
# pygame.draw.line(screen, (0, 0, 255), (639, 0), (0, 479))
# pygame.display.flip()


def initGrid(N):
	global screen, UNIT_SIDE
	screen = pygame.display.set_mode((SCREEN_SIDE, SCREEN_SIDE))
	UNIT_SIDE = int(SCREEN_SIDE/N)
	screen.fill(BLACK)


def connect(x1, y1, x2, y2):
	"""
	removes the wall between two cells and visit the new cell
	"""
	print(UNIT_SIDE)

	# remove wall
	if y1 == y2: # vertical wall between horizontally connected cells
		wallAbscissa = max(x2, x1)
		# pygame.draw.line(screen, WHITE, 
		# 	(wallAbscissa*UNIT_SIDE-2, y1*UNIT_SIDE-2),
		# 	(wallAbscissa*UNIT_SIDE-2, y1*(UNIT_SIDE+1)-2), width = 8)


		print("line: ", (wallAbscissa*UNIT_SIDE, y1*UNIT_SIDE),
			(wallAbscissa*UNIT_SIDE, (y1+1)*UNIT_SIDE))
		pygame.draw.line(screen, WHITE, 
			(wallAbscissa*UNIT_SIDE-1, y1*UNIT_SIDE+1),
			(wallAbscissa*UNIT_SIDE-1, (y1+1)*UNIT_SIDE-2), width = 3)


	elif x1 == x2:
		wallOrdinate = max(y1, y2)
		pygame.draw.line(screen, WHITE, 
			(x1*UNIT_SIDE+1, wallOrdinate*UNIT_SIDE-1),
			((x1+1)*UNIT_SIDE-2, wallOrdinate*UNIT_SIDE-1), width=3)

	# visit new cell
	print("filling", (x2*UNIT_SIDE+2, y2*UNIT_SIDE+2, UNIT_SIDE-2, UNIT_SIDE-2))
	pygame.draw.rect(screen, WHITE, (x2*UNIT_SIDE+1, y2*UNIT_SIDE+1, UNIT_SIDE-2, UNIT_SIDE-2))

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




N = 64
initGrid(N)

pygame.draw.rect(screen, WHITE, (1, 1, UNIT_SIDE-2, UNIT_SIDE-2))

drawMaze(N)





running = True
while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = False

"""
 idea: start with a grid with walls everywhere, then do a randomized depth first search that opens the walls

 Questions:
	+ How do we represent the maze as a matrix for solving ?
		-> Maybe for each cell store its connected neighbors 
	+ If we proceed by removing walls, what is (max_y, min_y) for a vertical wall and (max_x, min_x) for horizontal
		-> We can control the thikness of walls measured in units, this will be deduced by that

"""