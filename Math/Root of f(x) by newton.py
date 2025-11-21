"""
Newton iteration to approximate the root 
value of a function, we have function f(x)
and the derivative of f(x) is f_(x) and 
equation of tengent of f(x) at point xo.
the tangent line touches x-axis at some 
point and at that point we find a new 
value of xo and this operation repeat and 
approximate the value xo close to the 
root value of f(x).
equation of tengent on f(x) at point xo
y = x - f(xo)/f_(xo)
when tengent line touches x-axis value of 
y = 0 and by that we can calculate the 
value of x which is the new value of xo.
"""

def f(x):
	return x**3 - x +1
def f_(x):
	return 3*x**2 - 1

xo = -1

n = 0
while n <= 5:
	n += 1
	xo = xo - f(xo)/f_(xo)
	print(xo)