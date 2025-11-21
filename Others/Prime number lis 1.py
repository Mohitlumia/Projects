import math

def isPrime(n):
	for i in range(2, math.floor(math.sqrt(n))+1):
		if n%i == 0:
			return(False)
	return(True)

A = []
a = 100

for num in range(2, a):
	if isPrime(num) == True:
		A.append(num)

print(A)

