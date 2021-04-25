import pygame
from typing import Dict, Tuple, List
import random

N = 60
gridSide= (N+2)*(N+2)

prevDensity = [0.0 for _ in range(gridSide)] # using flattened array: perhaps better cache locality
density = [0.0 for _ in range(gridSide)]
prevVelocityX = [0.0 for _ in range(gridSide)]
velocityX = [0.0 for _ in range(gridSide)]
prevVelocityY = [3.0 for _ in range(gridSide)]
velocityY = [0.0 for _ in range(gridSide)]

dt = 0.2 #TODO: value ?




SCREEN_SIDE = 640
screen = None
CELL_SIDE = int(SCREEN_SIDE/N)




def initGrid():
	global screen, SCREEN_SIDE, CELL_SIDE
	screen = pygame.display.set_mode((SCREEN_SIDE, SCREEN_SIDE))
	screen.fill((0, 0, 0))



def index(i, j):
	return i + j*(N+2)



# def addSource(field: list[float], sources: dict[tuple[int, int], float]):
def addSource(field: List[float], sources: Dict[Tuple[int, int], float]):
	global dt
	# we will assume here few sources (which is the case generally)
	# we can work with dictionary and update only source locations
	# rather than iterating over the whole grid
	for (i, j), value in sources.items():
		field[index(i, j)] += value*dt


# def addSource(field: List[float], prevField: List[float]):
# 	for i in range((N+2)*(N+2)):
# 		field[i] += dt*prevField[i]


def diffuse(prevField: List[float], field: List[float], rate: float, onX: bool = False, onY: bool = False):
	global dt

	rate = rate * dt # Note: maybe rate need to adapt to size of N
	for _ in range(20): # number of iterations gauss seidel
		for i in range(1, N+1):
			for j in range(1, N+1):
				field[index(i, j)] = (prevField[index(i, j)] + (rate * (field[index(i, j-1)]+field[index(i-1, j)]+field[index(i+1, j)]+field[index(i, j+1)])))/(1+4*rate)

	# for i in range(1, N+1):
	# 	for j in range(1, N+1):
	# # 		print("initial: ", field[index(i, j-1)]+field[index(i-1, j)]+field[index(i+1, j)]+field[index(i, j+1)])
	# # 		print("with rate: ", (rate * (field[index(i, j-1)]+field[index(i-1, j)]+field[index(i+1, j)]+field[index(i, j+1)])/(1+4*rate)))
	# 		value = rate * (field[index(i, j-1)]+field[index(i-1, j)]+field[index(i+1, j)]+field[index(i, j+1)])/(1+4*rate)
	# 		if value > 1:
	# 			print(value)

	# for i in range(1, N+1):
	# 	for j in range(1, N+1):
	# 		print(field[index(i, j)])
	# Note: We can optimize the calls to index by initialising it before the for j loop and doing substractions
	# and additions on it for the indices of the neighbors

	setBoundaries(field, onX, onY)

	


def advect(prevField: List[float], field: List[float], velocityX: List[float], velocityY: List[float], onX: bool = False, onY: bool = False):
	# Note: maybe dt need to depend on N
	global dt
	for i in range(1, N+1):
		for j in range(1, N+1):
			x, y = i - velocityX[index(i,j)]*dt*N, j - velocityY[index(i,j)]*dt*N
			if x < 0.5: x = 0.5
			elif x > N+0.5: x = N+0.5
			if y < 0.5: y = 0.5
			elif y > N+0.5: y = N+0.5
			i0, j0 = int(x), int(y)
			i1, j1 = i0+1, j0+1
			# field at (i, j) = weighted average of field at i0,j0; i0,j0+1; i0+1,j0; i0+1,j0+1
			s1 = (x-i0)
			s0 = (1-s1) # = i0+1 - x
			t1 = (y-j0)
			t0 = (1-t1)
			# if i == (N+2)//2 and j == (N+2)//2:
			# print(s0, s1, t1, t0)
			field[index(i,j)] = s0*(t0*prevField[index(i0,j0)] + t1*prevField[index(i0,j1)]) + s1*(t0*prevField[index(i1,j0)] + t1*prevField[index(i1,j1)])

	setBoundaries(field, onX, onY)




def setBoundaries(field: List[float], onX=False, onY=False):
	for i in range(1, N+1):
		field[index(i, 0)] = -field[index(i, 1)] if (onY) else field[index(i, 1)] 
		field[index(i, N+1)] = -field[index(i, N)] if (onY) else field[index(i, N)]
		field[index(0, i)] = -field[index(1, i)] if (onX) else field[index(1, i)]
		field[index(N+1, i)] = -field[index(N, i)] if (onX) else field[index(N, i)]

	field[index(0, 0)] = 0.5*(field[index(0, 1)]+field[index(1, 0)])
	field[index(0, N+1)] = 0.5*(field[index(0, N)]+field[index(1, N+1)])
	field[index(N+1, 0)] = 0.5*(field[index(N, 0)]+field[index(N+1, 1)])
	field[index(N+1, N+1)] = 0.5*(field[index(N+1, N)]+field[index(N, N+1)])


def project():
	h = 1.0/N
	p = prevVelocityX
	div = prevVelocityY
	for i in range(1, N+1):
		for j in range(1, N+1):
			div[index(i,j)] = -0.5*h*(velocityX[index(i+1,j)]-velocityX[index(i-1,j)]+velocityY[index(i,j+1)]-velocityY[index(i,j-1)])
			p[index(i,j)] = 0

	setBoundaries(div)
	setBoundaries(p)

	for _ in range(20): # number of iterations gauss seidel
		for i in range(1, N+1):
			for j in range(1, N+1):
				p[index(i,j)] = (div[index(i,j)]+p[index(i-1,j)]+p[index(i+1,j)]+p[index(i,j-1)]+p[index(i,j+1)])/4
		setBoundaries(p)

	for i in range(1, N+1):
		for j in range(1, N+1):
			velocityX[index(i,j)] -= 0.5*(p[index(i+1,j)]-p[index(i-1,j)])/h;
			velocityY[index(i,j)] -= 0.5*(p[index(i,j+1)]-p[index(i,j-1)])/h;

	setBoundaries(velocityX, onX=True)
	setBoundaries(velocityY, onY=True)




def densityStep():
	densSources = {((N+2)//2, (N+2)//2): 2550} #TODO: value ?

	global velocityX, velocityY, density, prevDensity

	addSource(density, densSources)
	# addSource(density, prevDensity)
	# print("after adding source", prevDensity[index((N+2)//2, (N+2)//2)])
	density, prevDensity = prevDensity, density
	diffuse(prevDensity, density, rate = 0.1) #TODO: value ?
	# print("after diffuse ", prevDensity[index((N+2)//2, (N+2)//2)])
	density, prevDensity = prevDensity, density
	advect(prevDensity, density, velocityX, velocityY)
	# print("after advect ", prevDensity[index((N+2)//2, (N+2)//2)])



def velocityStep():
	# velSourceX = {((N+2)//2, (N+2)//2): random.uniform(-3,0)} #TODO: value ?
	velSourceX = {((N+2)//2, (N+2)//2): -3} #TODO: value ?
	# velSourceY = {((N+2)//2, (N+2)//2): random.uniform(-3,0)} #TODO: value ?

	global velocityX, prevVelocityX, velocityY, prevVelocityY
	addSource(velocityX, velSourceX)
	# addSource(velocityY, velSourceY)
	velocityX, prevVelocityX = prevVelocityX, velocityX
	velocityY, prevVelocityY = prevVelocityY, velocityY
	diffuse(prevVelocityX, velocityX, rate = 0.1, onX = True) #TODO: value ?
	diffuse(prevVelocityY, velocityY, rate = 0.1, onY = True) #TODO: value ?
	project()
	velocityX, prevVelocityX = prevVelocityX, velocityX
	velocityY, prevVelocityY = prevVelocityY, velocityY
	advect(prevVelocityX, velocityX, prevVelocityX, prevVelocityY, onX = True)
	advect(prevVelocityY, velocityY, prevVelocityX, prevVelocityY, onY = True)
	project()

	# for i in range(1, N+1):
	# 	for j in range(1, N+1):
	# 		print(velocityY[index(i, j)])




def drawDensity():
	global density, CELL_SIDE, screen
	for i in range(1, N+1):
		for j in range(1, N+1):
			if density[index(i, j)] > 255:
				color = (255, 255, 255)
			else:
				color = (density[index(i, j)], density[index(i, j)], density[index(i, j)])

			# print(color)
			pygame.draw.rect(screen, color, (j*CELL_SIDE, i*CELL_SIDE, CELL_SIDE, CELL_SIDE))
	pygame.display.flip()

	print("middle color: ", density[index((N+2)//2, (N+2)//2)])



initGrid()
# prevDensity[index((N+2)//2, (N+2)//2)] = 255
# density[index((N+2)//2, (N+2)//2)] = 0
fpsClock = pygame.time.Clock()
fpsClock.tick(40)
for _ in range(200):
	velocityStep()
	densityStep()
	drawDensity()


while True:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		pygame.quit()

