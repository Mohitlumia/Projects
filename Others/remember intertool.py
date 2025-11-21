from itertools import accumulate, takewhile, product, permutations

nums = list(accumulate(range(8)))
print(nums)
print('\n',list(takewhile(lambda x: x<= 10, nums)))


print('\nSimilar to..')# Similar to
print('\n',list(takewhile(lambda x: x<= 6, nums)))

print('\n',list(filter(lambda x: x<= 6, nums)))

def Mohit(m):
	for x in nums:
		if x > m:
			break
		yield x

print('\n',list(Mohit(6)))


def Priya(p):
	if (p > 0):
		p += Priya(p-1)
		print(p)
	return p


Priya(10)

def priya(P):
	while (P > 0):
		P -= 1
		yield P


print('\n',list(priya(10)))

letters = ("A", "B", "C")

print('\n',list(product(letters, list(priya(10)))))

print('\n', list(permutations(letters)))

print('\n', len(list(permutations(letters))))