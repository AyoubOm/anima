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
BLACK, WHITE, RED, GREEN = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0)

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



def addImage(images, basename):
	imagePath = "{}/{}_{}.png".format(TMP_DIR, basename, len(images)+1)
	pygame.image.save(screen, imagePath)
	img = Image.open(imagePath)
	images.append(img)



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
	addImage(images, "mazeGen")



def addEdge(graph, x1, y1, x2, y2):
	graph[x1][y1].add((x2, y2))
	graph[x2][y2].add((x1, y1))



def cellCenter(x, y):
	return (x*CELL_SIDE+int(CELL_SIDE/2), y*CELL_SIDE+int(CELL_SIDE/2))


def visit(x1, y1, x2, y2, images):
	pygame.draw.line(screen, GREEN, cellCenter(x1, y1), cellCenter(x2, y2), width=3)
	pygame.display.flip()
	addImage(images, "mazeSolve")


def invalidatePath(x1, y1, x2, y2, images):
	pygame.draw.line(screen, RED, cellCenter(x1, y1), cellCenter(x2, y2), width=3)
	pygame.display.flip()
	addImage(images, "mazeSolve")



def drawMaze(N):
	visited = set()
	stack = [(0, 0)]
	images = []
	graph = [[set() for _ in range(N)] for _ in range(N)] # store for each cell the neighbors it is connected to

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
			addEdge(graph, x, y, nx, ny)
			visited.add((nx, ny))
			stack.append((nx, ny))

	images[0].save('outputs/maze.gif', save_all=True, append_images=images[1:], optimize=False, loop=0)

	return graph



def solve(graph):
	def dfs(x, y, visited, visiting):
		visiting.add((x, y))

		pathFound = False
		neighbors = list(graph[x][y])
		neighbors.sort(key=lambda e: (-e[1], -e[0])) # go down or right first
		for nx, ny in neighbors:
			if (nx, ny) not in visited and (nx, ny) not in visiting:
				visit(x, y, nx, ny, images)
				if nx == N-1 and ny == N-1:
					return True
				pathFound = dfs(nx, ny, visited, visiting)
				if not pathFound:
					invalidatePath(x, y, nx, ny, images)
				else:
					break

		visiting.remove((x, y))
		visited.add((x, y))
		return pathFound


	images = []
	addImage(images, "mazeSolve") # the maze
	dfs(0, 0, set(), set())

	images[0].save('outputs/mazeSolve.gif', save_all=True, append_images=images[1:], optimize=False, loop=0)






def finish():
	shutil.rmtree(TMP_DIR)


N = 32
init(N)
mazeGraph = drawMaze(N)
solve(mazeGraph)


running = True
while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = False

finish()