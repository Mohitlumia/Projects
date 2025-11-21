# Lagrange‘s interpolation formula for unequi-spaced values

x = [-2, 0, 2]

y = [1, 5, 1]

value = 3

def lagrange(v):
	for j in range(len(y)):
		n = y[j]
		d = 1
		for i in range(len(y)):
			if i != j:
				n *= v - x[i]
				d *= x[j] - x[i]
		yield n/d

def submission(v):
	return sum(list(lagrange(v)))

print(submission(value))
