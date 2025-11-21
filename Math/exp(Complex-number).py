import math

def factorial(n):
	if n == 0:
		return 1
	else:
		return n*factorial(n-1)

def exp(x):
	return sum([
	x**n / factorial(n) for n in range(100)
	])

value = exp(complex(0, 1)*(math.pi)*(1/6))

print(value)
