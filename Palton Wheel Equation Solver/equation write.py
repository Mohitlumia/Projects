

file = open('file.py', 'w')


lis_Sym = []#list of symbol 
lis_Val = []#list of values

dic = {'v1': 'x', 'u1': 'x', 'a2': 'x', 'vw1': 'x', 'vw2': 'x', 'vr1': 'x', 'vr2': 'x', 'P_r': 'x', 'P_j': 'x', 'P_s': 'x', 'ef_h': 'x', 'ef_m': 'x', 'ef_v': 'x', 'ef_o': 'x', 'D': 'x', 'rmp': 'x', 'H': 'x', 'Q': 'x', 'k1': 1, 'k2': 1, 'g': 9.81, 'a1': 0, 'p': 1000, 'd': 'x', 'ar': 'x', 'nj': 1, 'cv': 1,'Qa': 'x','q':'x','w_b': 'x', 'd_b': 'x','n_b': 'x','m': 'x', 'K_u': 'x'}

eq = [
'eq1 = -vw1 + k1*v1*cos(a1)',
'eq2 = -vr1 + v1 - u1',
'eq3 = -vr2 + k2*vr1',
'eq4 = -vw2 - u1 + (vr2*cos(a2))',
'eq5 = -Q + (ar*v1)',
'eq6 = -P_r + nj*(p*Q*(vw1 + vw2)*u1)',
'eq7 = -P_j + nj*(p*Q*(v1**2))/2',
'eq8 = -ef_h + (P_r / P_j)',
'eq9 = -v1 + cv*((2*g*H)**(1/2))',
'eq10 = -u1 + (pi*rmp*D)/60',
'eq11 = -ef_m + (P_s/P_r)',
'eq12 = -ef_o + (P_s/P_j)',
'eq13 = -ar + (pi*(d**2))/4',
'eq14 = -ef_v + (Qa-q)/Q'
'eq15 = -w_b + (5*d)',
'eq16 = -d_b + (1.2*d)'
'eq17 = -n_b + 15 + D/(2*d)',
'eq18 = -m + D/d',
'eq19 = -K_u + u1/v1'
]

for i,j in dic.items():
	lis_Sym.append(i)
	lis_Val.append(j)


y = 'lis_Val = {}'.format(lis_Val)

z = ''
z1 = ''
for i in range(len(lis_Sym)-1):
	z += ('{}, '.format(lis_Sym[i]))
	z1 += ('\'{}\', '.format(lis_Sym[i]))
x = '{}{}'.format(z, lis_Sym[-1])
x = '{x} = symbols(\'{x}\')'.format(x=x)
z = ('lis_Sym = [{} {}]'.format(z, lis_Sym[-1]))
z1 = ('lis_Sym1 = [{} \'{}\']'.format(z1, lis_Sym[-1]))
I = '''
n = 0
while n != 1:
	s = input('sym:- ')
	if s == '1':
		n += 1
	v = input('val:- ')
	try:
		lis_Val[lis_Sym1.index(s)] = float(v)
		print('--------------')
	except ValueError:
		if n != 1:
			print('--ERROR OCCURS--')
'''

lis_Eq = []
lis_Eq_Val = []
e = ''
f = ''
g = ''
for i in range(len(eq)-1):
	e += ('{}\n'.format(eq[i]))
	eq[i] = eq[i].split(' ')
	f += ('{}, '.format(eq[i][0]))
	eq[i] = eq[i][2].split('-')
	#lis_Eq_Val.append(i[1])
	g += ('{}, '.format(eq[i][1]))

e += ('{}\n'.format(eq[-1]))
eq[-1] = eq[-1].split(' ')
f = 'lis_Eq = [{}{}]'.format(f, eq[-1][0])
eq[-1] = eq[-1][2].split('-')
g = 'lis_Eq_Val = [{}{}]'.format(g, eq[-1][1])

a = 'from sympy import symbols,Eq,cos,pi,pprint,solve'
b = '''
def Substitute(eq):
	# substitute value
	for i in range(len(lis_Val)):
		if str(type(lis_Val[i])) != str(type('x')):
			eq = eq.subs(lis_Sym[i],lis_Val[i])

	return eq

def Solve(eq):
	# add in solved value in lis_Val
	count = 0
	count_lis = 0
	for i in range(len(lis_Sym)):
		if str(lis_Sym[i]) in  str(eq):
			count += 1
			count_lis += i
	if count == 1:
		if type(solve(eq)[0]) != dict:
			lis_Val[count_lis] = solve(eq)[0]
			pprint(Eq(lis_Sym[count_lis],lis_Val[count_lis]))#pprint 

# number of opretion
for n in range(2):
	for i in range(len(lis_Eq)):
		lis_Eq[i] = Substitute(lis_Eq[i])
		Solve(lis_Eq[i])
		for j in range(len(lis_Eq)):
			lis_Eq[i] = (lis_Eq[i] + lis_Eq_Val[i]).subs(lis_Eq_Val[j], lis_Eq[j] + lis_Eq_Val[j]) - lis_Eq_Val[i]
		lis_Eq[i] = Substitute(lis_Eq[i])
		Solve(lis_Eq[i])
			
print('')
print('____Final Results____')
print('')

for i in range(len(lis_Sym)):
	print(lis_Sym[i],'=', lis_Val[i])
'''

file.write('{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}'.format(a,x,y,z,z1,I,e,f,g,b))
