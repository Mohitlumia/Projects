from sympy import symbols, solve, pi, cos, pprint, Eq


v1, u1, a2, vw1, vw2, vr1, vr2, P_r, P_j, P_s, ef_h, ef_m, ef_v, ef_o, D, rmp, H, Q, k1, k2, g, a1, p, d, ar, nj,  cv = symbols('v1, u1, a2, vw1, vw2, vr1, vr2, P_r, P_j, P_s, ef_h, ef_m, ef_v, ef_o, D, rmp, H, Q, k1, k2, g, a1, ρ, d, ar, nj,  cv')

symbol = [v1, u1, a2, vw1, vw2, vr1, vr2, P_r, P_j, P_s, ef_h, ef_m, ef_v, ef_o, D, rmp, H, Q, k1, k2, g, a1, p, d, ar, nj,  cv]

values = {v1 : 'x', u1 : 'x', a2 : 'x', vw1 : 'x', vw2 : 'x', vr1 : 'x', vr2 : 'x', P_r : 'x', P_j : 'x', P_s : 14715000, ef_h : 'x', ef_m : 'x', ef_v : 'x', ef_o : 'x', D : 'x', rmp : 'x', H : 500, Q : 'x', k1 : 1, k2 : 1, g : 9.81, a1 : 0, p : 1000, d : 0.15, ar : 'x', nj : 2, cv : 1}

equation = [{vw1 : k1*v1*cos(a1)},
						{vr1 : v1 - u1},
						{vr2 : k2*vr1},
						{vw2 : - u1 + (vr2*cos(a2))},
						{Q : (ar*v1)},
						{P_r : nj*(p*Q*(vw1 + vw2)*u1)},
						{P_j : nj*(p*Q*(v1**2))/2},
						{ef_h : (P_r / P_j)},
						{v1 : cv*((2*g*H)**(1/2))},
						{u1 : (pi*rmp*D)/60},
						{ef_m : (P_s/P_r)},
						{ef_o : (ef_m*ef_h)},
						{ar : (pi*(d**2))/4}]


class Solving:
	
	def __init__(self, symbols, equation, values):
		self.symbols = symbols
		self.equation = equation
		self.values = values
	
	def equal_Zero(self):
		lis = []
		for eq in self.equation:
			lis_key = list(map(lambda i : i ,eq))
			key = lis_key[0]
			eq = (eq[key] - key)
			lis.append(eq)
		self.equation = lis
		
	def Substitute(self):
		lis = []
		for eq in self.equation:
			for key, val in self.values.items():
				if type(val) != str:
					eq = eq.subs(key, val)
			lis.append(eq)
		self.equation = lis
	
	def one_Sym_Eq(self):
		for eq in self.equation:
			count = 0
			for sym in self.symbols:
				if str(sym) in str(eq):
					count += 1
					count_sym = sym
			if count == 1:
				yield count_sym, eq

	def Solve(self, one_sym_eq):
		for sym , eq in dict(one_sym_eq).items():
			sol = solve(eq)[0]
			self.values[sym] = sol
			pprint(Eq(sym, sol))

	def Print(self):
		for sym, val in self.values.items():
			print(sym,'=' ,val)


S = Solving(symbol, equation, values)
S.equal_Zero()
for n in range(3):
	S.Substitute()
	y = S.one_Sym_Eq()
	S.Solve(y)

print('\n____Final Results____\n')
S.Print()

