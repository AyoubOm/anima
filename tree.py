import matplotlib.pyplot as plt
from math import tan, pi, sqrt, atan
from random import uniform
import numpy as np


MAX_DEVIATION=pi/8 # child branch will be deviated from parent by maximum + or - this value
MAX_BRANCH_SIZE_RATIO = 0.8 # child branch has a length between MIN_BRANCH_SIZE_RATIO and MAX_BRANCH_SIZE_RATIO
MIN_BRANCH_SIZE_RATIO = 0.5


class Branch:
	def __init__(self, x1, y1, x2, y2):
		"""
		bottom and top are points represented as 2-elements array
		"""
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2

	def initFromCharacteristics(self, slope, length):
		x1 = self.x2
		y1 = self.y2
		if slope < 0:
			x2 = -length/sqrt(slope**2+1) + x1
		else:
			x2 = length/sqrt(slope**2+1) + x1
		y2 = slope*(x2-x1) + y1
		return Branch(x1, y1, x2, y2)

	def length(self):
		return sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2)

	def slope(self):
		if self.x1 == self.x2: return (self.y2-self.y1)/(self.x2-self.x1+0.00001) 
		return (self.y2-self.y1)/(self.x2-self.x1) # TODO: handle case x2 == x1




def tree(parent, depth, xs, ys):
	"""
	parent: is the root segment of the tree to be generated
	depth: number of branch levels of the tree
	"""
	if depth <= 0: return
	a = parent.slope()
	parentLength = parent.length()
	angle = atan(a)

	newSlope1 = tan(uniform(angle - MAX_DEVIATION, angle))
	newLength1 = parentLength*uniform(MIN_BRANCH_SIZE_RATIO, MAX_BRANCH_SIZE_RATIO)
	childBranch1 = parent.initFromCharacteristics(newSlope1, newLength1)
	xs.append(childBranch1.x2)
	ys.append(childBranch1.y2)
	tree(childBranch1, depth-1, xs, ys)

	xs.append(np.nan)
	ys.append(np.nan)

	xs.append(childBranch1.x1)
	ys.append(childBranch1.y1)


	newSlope2 = tan(uniform(angle, angle + MAX_DEVIATION))
	newLength2 = parentLength*uniform(MIN_BRANCH_SIZE_RATIO, MAX_BRANCH_SIZE_RATIO)
	childBranch2 = parent.initFromCharacteristics(newSlope2, newLength2)
	xs.append(childBranch2.x2)
	ys.append(childBranch2.y2)
	tree(childBranch2, depth-1, xs, ys)


xs = [0, 0]
ys = [0, 0.4]

tree(Branch(0, 0, 0, 0.4), 14, xs, ys)

plt.plot(xs, ys)
plt.show()






