
def fun(x):
	return x**2 - x - 1 # Equation 

# Regula-Falsi method
class F_method:
	
	def __init__(self, start, next):
		self.start = start
		self.next = next
		
	def loop(self, n = 10):
		while n > 0:
			n -= 1
			c = self.next - fun(self.next)*((self.next-self.start)/(fun(self.next)-fun(self.start)))
			print(c)
			if fun(self.start)*fun(c) < 0:
				self.next = c
			else:
				self.start = c

f = F_method(1,2)
f.loop()

