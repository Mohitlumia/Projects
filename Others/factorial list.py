lis = []
def factorial(n):
	if n == 0:
		return 1
	else:
		n *= factorial(n-1)
		lis.append(n)
		return n

factorial(10)
print(lis)

