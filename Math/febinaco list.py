def fun(x,n=0,j=1):
	while j <= x:
		n += j
		j += 1
		yield n

lis = list(fun(10))