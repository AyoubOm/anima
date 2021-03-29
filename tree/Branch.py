from math import sqrt


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
		return (self.y2-self.y1)/(self.x2-self.x1)
