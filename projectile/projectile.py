"""
TODO:

- one projectile animated position
- make previous positions transparent
- multiple projectiles with same starting positions but different velocity vectors
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



fig = plt.figure()
axes = plt.axes(xlim=(0, 300), ylim=(0, 200)) # in meters

class ProjectileAnimation:

	def __init__(self, projectiles):
		self.projectiles = projectiles
		for _ in range(len(projectiles)):
			self.currentPositions, = axes.plot([], [], 'o', color = (0, 0, 1, 1))
			self.previousPositions, = axes.plot([], [], 'o', color = (0, 0, 1, 0.2))

			self.currentPositions.set_data([], [])
			self.previousPositions.set_data([], [])

	# def init(self):
	# 	return self.previousPositions, self.currentPositions


	def update(self, i):
		deltaT = i * 0.5
		if self.currentPositions.get_xdata(): # = true from the second frame
			self.previousPositions.set_data(
				self.previousPositions.get_xdata() + self.currentPositions.get_xdata(),
				self.previousPositions.get_ydata() + self.currentPositions.get_ydata()
			)
		x, y = self.projectiles[0].position(deltaT)
		self.currentPositions.set_data([x], [y])
		return self.previousPositions, self.currentPositions


projectiles = [Projectile(5, 5, 20, 40)]
animation = ProjectileAnimation(projectiles)
FuncAnimation(fig, animation.update, frames=30, interval=100, blit=True)

plt.show()




