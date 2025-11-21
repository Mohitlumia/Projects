# For loop
n = 10
factorial = 1
for i in range(1, n + 1):
    factorial *= i
print('Factorial of %d is %d' % (n, factorial))

# While loop
x = 1
j = 1
while j <= 10:
	x *= j
	j += 1
print('Factorial of %d is %d' % (10, x))

# Recursion 
def fac(f):
	if f == 1:
		return 1
	else:
		return f*fac(f-1)
print('Factorial of %d is %d' % (10, fac(10)))