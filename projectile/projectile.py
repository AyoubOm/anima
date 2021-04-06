"""
simulation of a projectile motion using Newton's second law of motion.
Only gravitational force is considered
"""

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


	def velocityX(self, deltaT):
		return self.vx0

	def velocityY(self, deltaT):
		return abs(self.vy0 - gravityAcceleration*deltaT)


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

		self.vxText = plt.text(220, 170, "vx={} m/s".format(self.projectiles[0].vx0), fontsize=10, color=(float(1/N), 0, float(1/N)))
		self.vyText = plt.text(220, 160, "vy={} m/s".format(self.projectiles[0].vy0), fontsize=10, color=(float(1/N), 0, float(1/N)))




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

		self.vxText.set_text("vx={} m/s".format(self.projectiles[0].velocityX(deltaT)))
		self.vyText.set_text("vy={} m/s".format(round(self.projectiles[0].velocityY(deltaT), 2)))


		return self.previousPositions + self.currentPositions + (self.vxText, self.vyText)


projectiles = [Projectile(5, 5, 10, 60), Projectile(5, 5, 20, 40), Projectile(5, 5, 40, 30)]
animation = ProjectilesAnimation(projectiles, frames = 40, interval=300)

FuncAnimation(fig, animation.update, 
	frames=animation.frames, interval=animation.interval, blit=True).save('outputs/projectile.gif')


plt.show()




