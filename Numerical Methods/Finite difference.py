
#function
def fun(x):
	return x**2 - 4

#forward difference
class F_diff:
	
	def __init__(self, start,diff):
		self.start = start
		self.diff = diff
		
	def loop(self, fun, n=5):
		while n > 0:
			n -= 1
			f = fun
			f_ = (f(self.start+self.diff)-f(self.start))/(self.diff)
			xo = self.start - (f(self.start)/f_)
			self.start = xo
			print(self.start)


#backward differnce
class B_diff:
	
	def __init__(self, start,diff):
		self.start = start
		self.diff = diff
		
	def loop(self, fun, n=5):
		while n > 0:
			n -= 1
			f = fun
			f_ = (f(self.start+self.diff)-f(self.start))/(self.diff)
			xo = self.start - (f(self.start)/f_)
			self.start = xo
			print(self.start)


#center difference
class C_diff:
	
	def __init__(self, start,diff):
		self.start = start
		self.diff = diff
		
	def loop(self, fun, n=5):
		while n > 0:
			n -= 1
			f = fun
			f_ = (f(self.start+self.diff)-f(self.start))/(self.diff)
			xo = self.start - (f(self.start)/f_)
			self.start = xo
			print(self.start)


F = F_diff(3 ,0.001)
F.loop(fun)
print('')

B = B_diff(3 ,0.001)
B.loop(fun, 10)
print('')

C = C_diff(3 ,0.001)
C.loop(fun)
