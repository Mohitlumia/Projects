a = int(input('Enter a number:'))
b = int(input('Enter another number:'))
x = a*b

if b > a:
	a, b = b, a # it swaps the values


# Loop for LCM
for n in range(a, (x+1)):
	if n%a == n%b == 0:
		print('\n%d is the LCM of %d & %d' % (n, a, b))
		break
		
		
		
# Loop for HCF
for n in range(b, 0, -1):
	if b%n == a%n == 0:
		print('%d is the HCF of %d & %d' % (n, a, b))
		break