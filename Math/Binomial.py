def factorial(n):
	if n == 0:
		return 1
	else:
		return n*factorial(n-1)

def combination(a, b):
	return factorial(a)/(factorial(a-b)*factorial(b))

def Binomial(x, n):
	x -= 1
	return sum([
	combination(n, k)*(x**(n-k)) for k in range(n+1)
	])

print(Binomial(3,2))
