a = int(input('Enter a number:'))
b = int(input('Enter another number:'))

if b > a:
	a, b = b, a # it swaps the values

def HCF(p,q):
	while True:
		if p%q == 0:
			return q
		else:
			p, q = q, p%q


H = HCF(a, b)
print('%d is the HCF of %d & %d' % (H, a, b))

L = a*b / H
print('%d is the LCM of %d & %d' % (L, a, b))

