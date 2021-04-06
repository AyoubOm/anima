import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


gravityAcceleration = 9.81

class Projectile:

	def __init__(self, x0, y0, vx0, vy0):
		self.x0 = x0
		self.y0 = y0
		self.vx0 = vx0
		self.vy0 = vy0


	def position(self, deltaT):
		"""
		deltaT: time elapsed since the pojectile was thrown in unit of time
		"""
		x0 = self.x0
		y0 = self.y0
		vx0 = self.vx0
		vy0 = self.vy0
		return (vx0*deltaT + x0, -0.5*gravityAcceleration*(deltaT**2) + vy0*deltaT + y0)



fig = plt.figure()
axes = plt.axes(xlim=(0, 300), ylim=(0, 200)) # in meters

class ProjectilesAnimation:

	def __init__(self, projectiles, frames, interval):
		self.projectiles = projectiles
		self.frames = frames
		self.interval = interval
		self.currentPositions = () 
		self.previousPositions = () # each projectile has its line2D object
		N = len(projectiles)
		for i in range(N):
			color = (float(1/N)*(i+1), 0, float(1/N)*(i+1))
			self.currentPositions = self.currentPositions + (axes.plot([], [], 'o', color = color+(1, ))[0], )
			self.previousPositions = self.previousPositions + (axes.plot([], [], 'o', color = color+(0.2, ))[0], )


	def update(self, i):
		deltaT = i * float(self.interval / 1000) # period elapsed for the projectile time in seconds
		if i % self.frames > 1:
			for (previous, current) in zip(self.previousPositions, self.currentPositions):
				previous.set_data(
					previous.get_xdata() + current.get_xdata(),
					previous.get_ydata() + current.get_ydata())

		elif i % self.frames == 1: # clear the figure periodically
			for (previous, current) in zip(self.previousPositions, self.currentPositions):
				previous.set_data([], [])
				current.set_data([], [])

		for projectile, currentPos in zip(self.projectiles, self.currentPositions):
			x, y = projectile.position(deltaT)
			currentPos.set_data([x], [y])

		return self.previousPositions + self.currentPositions


projectiles = [Projectile(5, 5, 20, 40), Projectile(5, 5, 40, 30), Projectile(5, 5, 10, 60)]
animation = ProjectilesAnimation(projectiles, frames = 80, interval=200)

FuncAnimation(fig, animation.update, frames=animation.frames, interval=animation.interval, blit=True)

plt.show()




