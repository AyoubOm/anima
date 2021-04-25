from typing import Dict, Tuple, List
import random

N = 40
gridSide= (N+2)*(N+2)

prevDensity = [0.0 for _ in range(gridSide)] # using flattened array: perhaps better cache locality
density = [0.0 for _ in range(gridSide)]

prevDensity2 = [0.0 for _ in range(gridSide)] # using flattened array: perhaps better cache locality
density2 = [0.0 for _ in range(gridSide)]

prevVelocityX = [0.0 for _ in range(gridSide)]
velocityX = [0.0 for _ in range(gridSide)]
prevVelocityY = [0.0 for _ in range(gridSide)]
velocityY = [0.0 for _ in range(gridSide)]

dt = 0.1 #TODO: value ?

NB_ITER = 3

array = None



def index(i, j):
	return i + j*(N+2)



def addSource(field: List[float], sources: Dict[Tuple[int, int], float]):
	global dt
	# we will assume here few sources (which is the case generally)
	# we can work with dictionary and update only source locations
	# rather than iterating over the whole grid
	for (i, j), value in sources.items():
		field[index(i, j)] += value*dt




def diffuse(prevField: List[float], field: List[float], rate: float, onX: bool = False, onY: bool = False):
	global dt, NB_ITER

	a = rate * dt # Note: maybe rate need to adapt to size of N
	for _ in range(NB_ITER): # number of iterations gauss seidel
		for i in range(1, N+1):
			for j in range(1, N+1):
				field[index(i, j)] = (prevField[index(i, j)] + (a * (field[index(i, j-1)]+field[index(i-1, j)]+field[index(i+1, j)]+field[index(i, j+1)])))/(1+4*a)

	# Note: We can optimize the calls to index by initialising it before the for j loop and doing substractions
	# and additions on it for the indices of the neighbors

	setBoundaries(field, onX, onY)

	


def advect(prevField: List[float], field: List[float], velocityX: List[float], velocityY: List[float], onX: bool = False, onY: bool = False):
	# Note: maybe dt need to depend on N
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

	for _ in range(NB_ITER): # number of iterations gauss seidel
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
	source1 = ((N+2)//2, (N+2)//2)
	source2 = (2*(N+2)//3, (N+2)//3)

	densSources, densSources2 = {}, {}
	for i in range(1):
		densSources[(source1[0]+i, source1[1]+i)] = 2000.0

	# for i in range(3):
	# 	densSources2[(source2[0]+i, source2[1]+i)] = 2550.0

	global velocityX, velocityY, density, prevDensity
	global prevDensity2, density2

	addSource(density, densSources)
	density, prevDensity = prevDensity, density
	diffuse(prevDensity, density, rate = 0.5) #TODO: value ?
	density, prevDensity = prevDensity, density
	advect(prevDensity, density, velocityX, velocityY)

	# for i in range(1, N+1):
	# 	for j in range(1, N+1):
	# 		if density[index(i, j)] > 10:
	# 			print(density[index(i, j)])

	global array
	array = [[density[index(i, j)] for j in range(1, N+1)] for i in range(1, N+1)]


	# addSource(density2, densSources2)
	# density2, prevDensity2 = prevDensity2, density2
	# diffuse(prevDensity2, density2, rate = 0.01)
	# density2, prevDensity2 = prevDensity2, density2
	# advect(prevDensity2, density2, velocityX, velocityY)



def velocityStep():
	source1 = ((N+2)//2, (N+2)//2)

	velSourceX, velSourceY = {}, {}
	velSourceX[source1] = -2
	# velSourceY[source1] = -2.5


	global velocityX, prevVelocityX, velocityY, prevVelocityY
	addSource(velocityX, velSourceX)
	addSource(velocityY, velSourceY)
	velocityX, prevVelocityX = prevVelocityX, velocityX
	velocityY, prevVelocityY = prevVelocityY, velocityY
	diffuse(prevVelocityX, velocityX, rate = 0.5, onX = True) #TODO: value ?
	diffuse(prevVelocityY, velocityY, rate = 0.5, onY = True) #TODO: value ?
	project()
	velocityX, prevVelocityX = prevVelocityX, velocityX
	velocityY, prevVelocityY = prevVelocityY, velocityY
	advect(prevVelocityX, velocityX, prevVelocityX, prevVelocityY, onX = True)
	advect(prevVelocityY, velocityY, prevVelocityX, prevVelocityY, onY = True)
	project()





import matplotlib.pyplot as plt
from matplotlib import animation


def update(i):
	velocityStep()
	densityStep()
	im.set_array(array)

fig = plt.figure()

array = [[density[index(i, j)] for j in range(1, N+1)] for i in range(1, N+1)]
im = plt.imshow(array, cmap='gray', vmax=255, interpolation='bilinear')

anim = animation.FuncAnimation(fig, update, interval=0)
plt.show()