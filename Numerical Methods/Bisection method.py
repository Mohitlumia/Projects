
def fun(x):
	return x**2 - x - 1 # Equation 

# Bisection method
class B_method:
	
	def __init__(self, start, end, gap):
		self.start = start
		self.next = start + gap
		self.end = end
		self.gap = gap
		
	def check(self):
		# check opposite sign
		while fun(self.start)*fun(self.next) > 0 and self.next < self.end:
			self.start += self.gap
			self.next += self.gap
	
	def loop(self, n = 10):
		while n >= 0:
			n -= 1
			x = (self.start + self.next)/2
			print(x)
			if fun(self.start)*fun(x) < 0:
				self.next = x
			else:
				self.start = x


b = B_method(-50, 50, 0.1)
b.check()
b.loop(5)

