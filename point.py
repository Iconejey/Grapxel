class Point:
	def __init__(self, x = 0, y = 0):
		self.x, self.y = x, y


	def __str__(self):
		return f'Point({self.x}, {self.y})'

	
	def __add__(self, other):
		if type(other) == Point:
			x = self.x + other.x
			y = self.y + other.y
		else:
			x = self.x + other[0]
			y = self.y + other[1]
		return Point(x, y)

	
	def __sub__(self, other):
		if type(other) == Point:
			x = self.x - other.x
			y = self.y - other.y
		else:
			x = self.x - other[0]
			y = self.y - other[1]
		return Point(x, y)


	def __pos__(self):
		return Point(+self.x, +self.y)


	def __neg__(self):
		return Point(-self.x, -self.y)


	def __mul__(self, scale):
		return Point(self.x*scale, self.y*scale)


	def __div__(self, scale):
		return Point(self.x/scale, self.y/scale)
	

	def __floordiv__(self, scale):
		return Point(self.x//scale, self.y//scale)


	def __abs__(self):
		return (self.x**2 + self.y**2)**.5


	def __iter__(self):
		return iter(self.getCoords())


	def getCoords(self, integer = False):
		pos = self.x, self.y
		return tuple(map(int, pos)) if integer else pos