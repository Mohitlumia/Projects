from sympy import symbols,Eq,cos,pi,pprint,solve

v1, u1, a2, vw1, vw2, vr1, vr2, P_r, P_j, P_s, ef_h, ef_m, ef_v, ef_o, D, rmp, H, Q, k1, k2, g, a1, p, d, ar, nj, cv = symbols('v1, u1, a2, vw1, vw2, vr1, vr2, P_r, P_j, P_s, ef_h, ef_m, ef_v, ef_o, D, rmp, H, Q, k1, k2, g, a1, ρ, d, ar, nj, cv')

lis_Val = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 1, 1, 9.81, 0, 1000, 'x', 'x', 1, 1]

lis_Sym = [v1, u1, a2, vw1, vw2, vr1, vr2, P_r, P_j, P_s, ef_h, ef_m, ef_v, ef_o, D, rmp, H, Q, k1, k2, g, a1, p, d, ar, nj,  cv]

lis_Sym1 = ['v1', 'u1', 'a2', 'vw1', 'vw2', 'vr1', 'vr2', 'P_r', 'P_j', 'P_s', 'ef_h', 'ef_m', 'ef_v', 'ef_o', 'D', 'rmp', 'H', 'Q', 'k1', 'k2', 'g', 'a1', 'p', 'd', 'ar', 'nj',  'cv']


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


eq1 = -vw1 + k1*v1*cos(a1)
eq2 = -vr1 + v1 - u1
eq3 = -vr2 + k2*vr1
eq4 = -vw2 - u1 + (vr2*cos(a2))
eq5 = -Q + (ar*v1)
eq6 = -P_r + nj*(p*Q*(vw1 + vw2)*u1)
eq7 = -P_j + nj*(p*Q*(v1**2))/2
eq8 = -ef_h + (P_r / P_j)
eq9 = -v1 + cv*((2*g*H)**(1/2))
eq10 = -u1 + (pi*rmp*D)/60
eq11 = -ef_m + (P_s/P_r)
eq12 = -ef_o + (ef_m*ef_h)
eq13 = -ar + (pi*(d**2))/4


lis_Eq = [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11, eq12, eq13]

lis_Eq_Val = [vw1, vr1, vr2, vw2, Q, P_r, P_j, ef_h, v1, u1, ef_m, ef_o, ar]


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
