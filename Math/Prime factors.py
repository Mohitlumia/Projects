# Here we get prime factor of a number

a = input("Enter the number for prime factor: ") 
a = int(a)

list_P = [] # list of prime number 
list_PF =[] # list of prime factor 

for n in range(2, a+1):
	for x in range(2, n):
		if n % x == 0:
			break
	else:
		list_P.append(n)

#print(list_P)
# divide the number with prime numbers in list_p

for i in range(len(list_P)):
	while a % list_P[i] == 0:
		list_PF.append(list_P[i])
		a /= list_P[i]

print('\n' , list_PF)
