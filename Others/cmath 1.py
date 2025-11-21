import cmath
# CMATH stand for Complex Math



# abs shows the length of the modulus
# cmath does not have any function to get a modulus alone.
print(abs(-1 + 0j))
# phase shows the radian at which the modulus is tilde
# (theta = atan2(y, x)) = phase opretion
# print(math.atan2(0, -1))
print(cmath.phase(complex(-1.0, 0.0)))
# first digit repersent length on real x-axis
# second digit repersent lenth on imaginary y-axis
# (cmath.polar) gives the hypotenuse/modulus of x and y-axis and radian in counter-clockwise
print(cmath.polar(-1 + 0j))
# polar and rect are oposite to each other
# rect takes the value of modulus and radian and give cordinate in x and y axis real and imaginary respectivly.
#(1 * math.cos(phi) + (math.sin(phi) * 1j)
print(cmath.rect(1, 3.141592653589793))
# Value of e raised to the power ()
print(cmath.exp(1))
# log(x, base) log of x to the given base.
print(cmath.log(8, 2))
# log of 2 with base of 10
print(cmath.log10(2))
# squre root
print(cmath.sqrt(-4))
# Trigonometric function
print(cmath.cos(-1))
print(cmath.sin(1))
print(cmath.tan(1))
# we use "a" before the trigonometric function like "acos(x)" to show inverse of cosine of x. same for all
print(cmath.acos(-1))
print(cmath.asin(1))
print(cmath.atan(1))
# Hyperbolic trigonometric function
print(cmath.cosh(-1))
print(cmath.sinh(1))
print(cmath.tanh(0))
# and inverse Hyperbolic trigonometric function
print(cmath.acosh(-1))
print(cmath.asinh(1))
print(cmath.atanh(0))
