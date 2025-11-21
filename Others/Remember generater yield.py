def countdown():
	i = 10
	while i > 0:
		yield i
		i -= 1

for n in countdown():
	print(n)
print(list(countdown()))