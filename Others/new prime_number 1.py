a = int(input("Enter number : -  "))

x = []
y = []
z = []

for i in range(2, a):
	x.append(i)


for i in range(len(x)):
	try:
		a = x.index(x[0]*x[0])

		for m in range(1, a):
			y.append(x[m])
		
		for n in range(1, len(x)-a):
			if x[a+n] % x[0] != 0:
				y.append(x[a+n])
			if x[0] * x[0] > x[-1]:
				break

		else:
			z.append(x[0])

		if len(x) > len(y):
			x, y = y, x
		y.clear()
	
	except Exception:
		break


print(z+y+x)
