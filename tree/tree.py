"""
Python script that draws a random tree and displays it using matplotlib

The random properties are:
	+ The angle of the child branches given parent branch angle: Generated between [angle-MAX_DEVIATION, angle+MAX_DEVIATION]
	with a uniform distribution 
	+ The length of the child branches given parent branch length: Generated between [MIN_BRANCH_SIZE_RATIO*parent_length, MAX_BRANCH_SIZE_RATIO*parent_length]

depth is also an input parameter of the function which is the number of branch levels in the tree

You can change these values and see the effect on the generated trees.

For further explanation: https://ayoubomari.medium.com/random-tree-generator-using-python-68a357e012ca
"""

import matplotlib.pyplot as plt
from math import tan, pi, sqrt, atan
from random import uniform
import numpy as np
from Branch import Branch

MAX_DEVIATION=pi/8
MAX_BRANCH_SIZE_RATIO = 0.8
MIN_BRANCH_SIZE_RATIO = 0.5


def tree(parent, depth, xs, ys):
	"""
	parent: is the root segment of the tree to be generated
	depth: number of branch levels of the tree

	the function adds generated branches extremities to params xs an ys
	"""
	if not xs:
		xs += [parent.x1, parent.x2]
		ys += [parent.y1, parent.y2]

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

xs, ys = [], []
tree(Branch(0, 0, 0, 0.4), 14, xs, ys)

plt.plot(xs, ys)
plt.show()





