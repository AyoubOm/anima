"""
Fluid simulation using Navier-Stokes based on paper Real-Time Fluid Dynamics for Games by Jos Stam
"""

from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
from matplotlib import animation
import random
import sys

N = 40
gridSide= (N+2)*(N+2)

prevDensity = [0.0 for _ in range(gridSide)] # using flattened array: perhaps better cache locality
density = [0.0 for _ in range(gridSide)]

prevVelocityX = [0.0 for _ in range(gridSide)]
velocityX = [0.0 for _ in range(gridSide)]
prevVelocityY = [0.0 for _ in range(gridSide)]
velocityY = [0.0 for _ in range(gridSide)]

dt = 0.2
viscosity, diffRate = None, None

nbIter = 3 # number of iterations for convergence - gauss seidel

screen = None


def index(i, j):
	return i + j*(N+2)


def addSource(field: List[float], sources: Dict[Tuple[int, int], float]):
	global dt
	for (i, j), value in sources.items():
		field[index(i, j)] += value*dt




def diffuse(prevField: List[float], field: List[float], rate: float, onX: bool = False, onY: bool = False):
	global dt, nbIter

	a = rate * dt * N * N
	for _ in range(nbIter): 
		for i in range(1, N+1):
			for j in range(1, N+1):
				field[index(i, j)] = (prevField[index(i, j)] + (a * (field[index(i, j-1)]+field[index(i-1, j)]+field[index(i+1, j)]+field[index(i, j+1)])))/(1+4*a)

	# Note: We can optimize the calls to index by initialising it before the for j loop and doing substractions
	# and additions on it for the indices of the neighbors
	setBoundaries(field, onX, onY)

	


def advect(prevField: List[float], field: List[float], velocityX: List[float], velocityY: List[float], onX: bool = False, onY: bool = False):
	global dt
	dt0 = dt*N
	for i in range(1, N+1):
		for j in range(1, N+1):
			x, y = i - velocityX[index(i,j)]*dt0, j - velocityY[index(i,j)]*dt0
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

	for _ in range(nbIter):
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




def densityStep(iteration):
	source1 = ((N+2)//2, (N+2)//2)
	densSources = {}

	for i in range(3):
		for j in range((4-i)//2):
			densSources[(source1[0]+i-1, source1[1]+j-1)] = 2500.0

	global velocityX, velocityY, density, prevDensity, screen

	addSource(density, densSources)
	density, prevDensity = prevDensity, density
	diffuse(prevDensity, density, rate = diffRate)
	density, prevDensity = prevDensity, density
	advect(prevDensity, density, velocityX, velocityY)

	screen = [[density[index(i, j)] for j in range(1, N+1)] for i in range(1, N+1)]



def velocityStep(iteration):
	source1 = ((N+2)//2, (N+2)//2)

	velSourceX, velSourceY = {}, {}

	for i in range(3):
		for j in range((4-i)//2):
			if iteration % 200 < 50:	
				velSourceX[(source1[0]+i-1, source1[1]+j-1)] = -1
				velSourceY[(source1[0]+i-1, source1[1]+j-1)] = -2
			elif iteration % 200 < 100:
				velSourceX[(source1[0]+i-1, source1[1]+j-1)] = 1
				velSourceY[(source1[0]+i-1, source1[1]+j-1)] = -2
			elif iteration % 200 < 150:
				velSourceX[(source1[0]+i-1, source1[1]+j-1)] = 1
				velSourceY[(source1[0]+i-1, source1[1]+j-1)] = 2
			else:
				velSourceX[(source1[0]+i-1, source1[1]+j-1)] = -1
				velSourceY[(source1[0]+i-1, source1[1]+j-1)] = 2

	global velocityX, prevVelocityX, velocityY, prevVelocityY, viscosity
	addSource(velocityX, velSourceX)
	addSource(velocityY, velSourceY)
	velocityX, prevVelocityX = prevVelocityX, velocityX
	velocityY, prevVelocityY = prevVelocityY, velocityY
	diffuse(prevVelocityX, velocityX, rate = viscosity, onX = True)
	diffuse(prevVelocityY, velocityY, rate = viscosity, onY = True)
	project()
	velocityX, prevVelocityX = prevVelocityX, velocityX
	velocityY, prevVelocityY = prevVelocityY, velocityY
	advect(prevVelocityX, velocityX, prevVelocityX, prevVelocityY, onX = True)
	advect(prevVelocityY, velocityY, prevVelocityX, prevVelocityY, onY = True)
	project()





def update(i):
	velocityStep(i)
	densityStep(i)
	im.set_array(screen) #TODO: this can be optimized by working with 2d arrays from the beginning



if __name__ == '__main__':
	colorMap = None
	if len(sys.argv)<=1 or sys.argv[1] == "fire_air":
		colorMap = "hot"
		viscosity = 0.0
		diffRate = 0.0
		dt = 0.21

	elif len(sys.argv)>=2 and sys.argv[1] == "smoke_air":
		colorMap = "binary"
		viscosity = 0.0
		diffRate = 0.0001
		dt = 0.1

	elif len(sys.argv)>=2 and sys.argv[1] == "ink_water":
		colorMap = "cool"
		viscosity = 0.0005
		diffRate = 0.0
		dt = 0.1

	else:
		print("usage: {} fire_air|smoke_air|ink_water".format(sys.argv[0]))
		sys.exit()

	fig = plt.figure()

	screen = [[density[index(i, j)] for j in range(1, N+1)] for i in range(1, N+1)]
	im = plt.imshow(screen, cmap=colorMap, vmax=500, interpolation='bilinear')

	anim = animation.FuncAnimation(fig, update, interval=0)
	plt.show()
