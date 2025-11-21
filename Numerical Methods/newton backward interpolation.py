x = [45, 50, 55, 60]

y = [0.7071, 0.7660, 0.8192, 0.8660]

x = x[::-1]
y = y[::-1]

def choose(u, i):
	m = 1
	n = 1
	for j in range(0, i):
		m *= (u-j)
		n *= (i-j)
	return m/n

def delta(p, lis):
	if p == 0:
		return lis[0]
	else:
		y0 = []
		for i in range(1, len(lis)):
			a = lis[i] - lis[i-1]
			y0.append(a)
		p -= 1
		return delta(p, y0)

#print(Choose(5,2))
print(delta(2, y))

value = 52

u = (value - x[0])/(x[1]-x[0])

sigma = sum([choose(u, i)*delta(i, y) for i in range(len(x))])

print("Value at %s is %s"%(value, round(sigma,6)))

