from random import seed, uniform

# seed(100011)

def fill(maze, unit, minX, maxX, minY, maxY):
	if (maxX-minX)/unit < 2 or (maxY-minY)/unit < 2:
		return
	# print(int(minX/unit), int(maxX/unit), int(minY/unit), int(maxY/unit))
	# print(minX, maxX, minY, maxY)

	splitAtX = uniform(minX+unit, maxX-unit)
	splitAtY = uniform(minY+unit, maxY-unit)

	x, y = int(splitAtX/unit), int(splitAtY/unit)
	# print("x=",x, "y=", y)

	holeHorizontal1 = uniform(minX, splitAtX-unit)
	holeHorizontal2 = uniform(splitAtX+unit, maxX)

	holeVertical1 = uniform(minY, splitAtY-unit)
	holeVertical2 = uniform(splitAtY+unit, maxY)

	# print(int(holeHorizontal1/unit), int(holeHorizontal2/unit))
	# print(int(holeVertical1/unit), int(holeVertical2/unit))

	for j in range(int(minX/unit), int(maxX/unit)+1):
		if j != int(holeHorizontal1/unit) and j != int(holeHorizontal2/unit):
			print(j)
			maze[y][j] = 1

	for i in range(int(minY/unit), int(maxY/unit)+1):
		if i != int(holeVertical1/unit) and i!=int(holeVertical2/unit):
			maze[i][x] = 1

	print(maze)

	fill(maze, unit, minX, splitAtX-unit, minY, splitAtY-unit)
	fill(maze, unit, splitAtX+unit, maxX, minY, splitAtY-unit)
	fill(maze, unit, minX, splitAtX-unit, splitAtY+unit, maxY)
	fill(maze, unit, splitAtX+unit, maxX, splitAtY+unit, maxY)
		




def generateMaze(size):
	minX, maxX = 0, 2
	minY, maxY = 0, 2
	unit = max(maxX-minX, maxY-minY) / size
	N, M = int((maxX-minX)/unit), int((maxY-minY)/unit)

	maze = [[0 for _ in range(N)] for _ in range(M)]
	fill(maze, unit, minX, maxX-unit, minY, maxY-unit)
	print(maze)
	return maze


generateMaze(8)

