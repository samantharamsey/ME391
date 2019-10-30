# -*- coding: utf-8 -*-
'''
Created on Sat Aug 31 08:13:40 2019
@author: sramse18

Root finding methods for single variable functions
'''

import numpy as np


def function(x):
    f = np.log(x) - np.sin(x)
    return f

def f1(x, y):
    f = y - x**2 - x + 6
    return f

def f2(x, y):
    g = y**2 + x**2 - 25
    return g

def bisection_method(x1, x2, tolerance):
    '''
    Determines the roots of a non-linear single variable function using the 
    method of bisections
    Args:
        x1 - initial guess which gives a negative solution to the function
        x2 - initial guess which gives a position solution to the fucntion
        tolerance - the tolerance for convergance
    '''
    f1 = function(x1)
    f2 = function(x2)
    if f1*f2 > 0:
        print('Error: Please choose different initial condition estimates')
    else:
        residual = abs(f1 - f2)
        iteration = 1
        print('%-13s %-20s %-20s %-20s' 
              %('Iterations', 'Function Value', 'Root Value', 'Residual'))
        while residual > tolerance:
            xn = (x1 + x2)/2
            fn = function(xn)
            if f1*fn > 0:
                x1 = xn
                f1 = fn
            else:
                x2 = xn
                f2 = fn
            residual = abs(fn)
            print('%5.1f %20.10f %20.10f %20.10f' 
                  %(iteration, fn, xn, residual))
            iteration = iteration + 1
        
        
def newton_method(x0, step_size, tolerance):
    '''
    Determines the roots of a non-linear single variable function using 
    derivative estimation and Taylor Series Expansion
    Args:
        x0 - initial condition estimate
        tolerance - the tolerance for convergence
        step_size - determines the size of delta x
    '''
    f0 = function(x0)
    residual = abs(f0)
    iteration = 1
    fx = (function(x0 + step_size) - f0) / step_size
    print('%-13s %-20s %-20s %-20s' 
          %('Iterations', 'Function Value', 'Root Value', 'Residual'))
    while residual > tolerance:
        x1 = x0 + ((0 - f0)/fx)
        f1 = function(x1)
        residual = abs(f1)
        f0 = f1
        x0 = x1
        fx = (function(x0 + step_size) - f0) / step_size
        print('%5.1f %20.10f %20.10f %20.10f' 
              %(iteration, f1, x1, residual))
        iteration = iteration + 1
    

def secant_method(alpha, x0, x1, tolerance):
    '''
    Determines the roots of a non-linear single variable function using 
    derivative estimation and Taylor Series Expansion
    Args:
        alpha - value of the function 
        x0 - initial condition estimate
        x1 - second initial condition estimate
        tolerance - the tolerance for convergence
    '''
    f0 = function(x0)
    f1 = function(x1)
    residual = 1
    iteration = 1
    print('%-13s %-20s %-20s %-20s' 
          %('Iterations', 'Function Value', 'Root Value', 'Residual'))
    
    if f0 < f1:
        x0, x1 = x1, x0
        f0 = function(x0)
        f1 = function(x1)
        
    while residual > tolerance:  
        df1 = ((f1 - f0)/(x1 - x0))
        x2 = x1 + ((alpha - f1)/df1)
        x0 = x1
        x1 = x2
        f0 = function(x0)
        f1 = function(x1)
        residual = abs(alpha - f1)
        print('%5.1f %20.10f %20.10f %20.10f' 
              %(iteration, f1, x1, residual))
        iteration = iteration + 1
    
    
def multi_newton(alpha, x0, y0, tolerance, step_size):
    
    iteration = 1
    residual = 1
    
    while residual > tolerance:
        
        f0 = f1(x0, y0)
        dfdx = f1(x0 + step_size, y0)
        dfdy = f1(x0, y0 + step_size)
        
        g0 = f2(x0, y0)
        dgdx = f2(x0 + step_size, y0)
        dgdy = f2(x0, y0 + step_size)
    
        b = np.array([[alpha - f0], [alpha - g0]])
        J = np.array([[(dfdx - f0)/step_size, (dfdy - f0)/step_size],
                     [(dgdx - g0)/step_size, (dgdy - g0)/step_size]])
        
        delta = J/b
        x0 = x0 + delta[0][0]
        y0 = y0 + delta[0][1]
        
        residual = abs(f0 - g0)
        print('%5.1f %20.10f %20.10f %20.10f %20.10f' 
              %(iteration, f0, x0, y0, residual))

        iteration = iteration + 1
    
    
if __name__ == '__main__':

    print('---------------------------- Bisection Method ----------------------------')
    bisection_result = bisection_method(0, 1, 10**-5)
    print(' ')
    print('----------------------------- Newton Method ------------------------------')
    newton_result = newton_method(0, 10**-8, 10**-5)
    print(' ')
    print('----------------------------- Secant Method ------------------------------')
    secant_result = secant_method(0.601, 0.3, 0.7, 10**-5)  
#    print(' ')
#    print('----------------------------- Multi Newton Method ------------------------------')
#    newton_result = multi_newton(0, 1, 1, 10**-5, 10**-8) 
    