import pygame

N = 20
gridSide= (N+2)*(N+2)

prevDensity = [0 for _ in range(gridSide)] # using flattened array: perhaps better cache locality
density = [0 for _ in range(gridSide)]
prevVelocityX = [0 for _ in range(gridSide)]
velocityX = [0 for _ in range(gridSide)]
prevVelocityY = [0 for _ in range(gridSide)]
velocityY = [0 for _ in range(gridSide)]

dt = 0.1

sources = {((N+2)//2, (N+2)//2): 1}


def densityStep():
	addSource(density, sources)
	density, prevDensity = prevDensity, density
	diffuse(prevDensity, density, 0.1, False)
	density, prevDensity = prevDensity, density
	advect(prevDensity, density, velocityX, velocityY)





def velocityStep():
	@TODO
	pass



def drawDensity():
	# Maybe we can draw directly once density for each cell is completely computed
	# without the reiteration
	@TODO
	pass



def index(i, j):
	return i + j*(N+2)



def addSource(field: list[float], sources: dict[tuple[int, int], float]):
	# we will assume here few sources (which is the case generally)
	# we can work with dictionary and update only source locations
	# rather than iterating over the whole grid
	for (i, j), value in sources.items():
		field[index(i, j)] += value*dt




def diffuse(prevField: list[float], field: list[float], rate: float, isVelocity: bool):
	rate = rate * dt # Note: maybe rate need to adapt to size of N
	for _ in range(20): # number of iterations gauss seidel
		for i in range(1, N+1):
			for j in range(1, N+1):
				field[index(i, j)] = prevField[index(i, j)] + rate * (field[index(i, j-1)] + field[index(i-1, j)] + field[index(i+1, j)] + field[index(i, j+1)]) / (1+4*rate)

	# Note: We can optimize the calls to coupleToIndex by initialising it before the for j loop and doing substractions
	# and additions on it for the indices of the neighbors

	if isVelocity: setBoundaries(field)


def advect(prevDensity: list[float], density: list[float], velocityX: list[float], velocityY: list[float]):
	# Note: maybe dt need to depend on N
	for i in range(1, N+1):
		for j in range(1, N+1):
			x, y = i - velocityX[index(i,j)]*dt, j - velocityY[index(i,j)]*dt
			if x < 0.5: x = 0.5
			if y < 0.5: y = 0.5
			i0, j0 = int(x), int(y)
			i1, j1 = i0+1, j0+1
			# density = weighted average of densities in i0,j0; i0,j0+1; i0+1,j0; i0+1,j0+1
			s1 = x-i0
			s0 = 1-s1
			t1 = y-j0
			t0 = 1-t1
			density[index(i,j)] = s0*(t0*prevDensity[index(i0,j0)] + t1*prevDensity[index(i0,j1)]) + s1*(t0*prevDensity[index(i1,j0)] + t1*prevDensity[index(i1,j1)])




def setBoundaries(field: list[float]):
	@TODO
	pass


def project():
	@TODO
	pass




for _ in range(100):
	velocityStep()
	densityStep()
	drawDensity()


while True:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		pygame.quit()
