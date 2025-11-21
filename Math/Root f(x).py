import sys
import math

def sign(a,b): #compares the sign of two numbers: sign > 0 iff a and b have same sign
    return a*b
 
       
def Bisection(xl, xr, tol):
    n = 1
    NMAX = 50
    while n <= NMAX: # limit iterations to prevent infinite loop
        error = abs(xl-xr)/2 #defines error measure
        c = (xr+xl)/2 # midpoint
        if f(c) == 0 or error < tol: # solution found
            print(c)
            return c
           
        n = n + 1 # increment step counter
        if sign(f(c),f(xl)) >= 0:
            print(c)
            xl = c
        else:
            xr = c # new interval            
            print(c)
            
    return c
   
 
def f(x):
    return math.sin(math.pi*x)-x

xl = 0.0
xr = 1.0
tol = 0.0001

Bisection(xl, xr, tol)
    
   