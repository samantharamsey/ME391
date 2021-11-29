# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:13:12 2021

@author: saman
"""

import numpy as np
import matplotlib.pyplot as plt


def sweep(x, AR, lam, sweep_LE):
    sweep = np.arctan(np.tan(sweep_LE) - (4/AR)*(x*(1 - lam)/(1 + lam)))
    return sweep

def sweep_LE(x, AR, lam, sweep):
    LE = np.arctan(np.tan(sweep) + (4/AR)*(x*(1 - lam)/(1 + lam)))
    return LE

def cp(y, sweep):
    l1 = 0.75*rc
    x1 = y*np.tan(sweep) + l1
    return (x1, y)

def coord(y, sweep):
    l1 = 0.25*rc
    x1 = y*np.tan(sweep) + l1
    return (x1, y)

def plot(lst, color = None):
    x, y = zip(*lst)
    plt.plot(x, y, c = color)
    
def wmn(xm, x1n, x2n, ym, y1n, y2n):
    term1 = (1/((xm - x1n)*(ym - y2n) - (xm - x2n)*(ym - y1n)))
    term2 = ((x2n - x1n)*(xm - x1n) + (y2n - y1n)*(ym - y1n))/(np.sqrt((xm - x1n)**2 + (ym - y1n)**2))
    term3 = ((x2n - x1n)*(xm - x2n) + (y2n - y1n)*(ym - y2n))/(np.sqrt((xm - x2n)**2 + (ym - y2n)**2))
    term4 = (1/(y1n - ym))*(1 + ((xm - x1n)/(np.sqrt((xm - x1n)**2 + (ym - y1n)**2))))
    term5 = (1/(y2n - ym))*(1 + ((xm - x2n)/(np.sqrt((xm - x2n)**2 + (ym - y2n)**2))))
    return term1*(term2 - term3) + term4 - term5
 

if __name__ == '__main__':
    
    # sweep angle at the 1/4 chord
    sweep_25 = 45*(np.pi/180)
    # taper ratio
    lam = 0.5
    # aspect ratio
    AR = 5
    # root chord
    rc = 4/15
    
    # distance between the panels
    x = 0.125
    # distance to the panel mid point
    x1 = x/2
    
    # sweep angle at the leading edge
    sweep_LE  = sweep_LE(0.25, AR, lam, sweep_25)
    # sweep angle at the 3/4 chord
    sweep_75  = sweep(0.75, AR, lam, sweep_LE)
    # sweep angle at the trailing edge
    sweep_100 = sweep(1.0, AR, lam, sweep_LE)
    
    cp1 = cp(x1,       sweep_75)
    cp2 = cp(x1 + x,   sweep_75)
    cp3 = cp(x1 + x*2, sweep_75)
    cp4 = cp(x1 + x*3, sweep_75)
    
    n1  = coord(0,     sweep_25)
    n2  = coord(x,     sweep_25)
    n3  = coord(x*2,   sweep_25)
    n4  = coord(x*3,   sweep_25)
    
    m1  = coord(x,     sweep_25)
    m2  = coord(x*2,   sweep_25)
    m3  = coord(x*3,   sweep_25)
    m4  = coord(x*4,   sweep_25)
    
    # # example data
    # xm  = np.array([0.2125, 0.3375, 0.4625, 0.5875])
    # ym  = np.array([0.0625, 0.1875, 0.3125, 0.4375])
    # x1n = np.array([0.0500, 0.1750, 0.3000, 0.4250])
    # y1n = np.array([0.0000, 0.1250, 0.2500, 0.3750])
    # x2n = np.array([0.1750, 0.3000, 0.4250, 0.5500])
    # y2n = np.array([0.1250, 0.2500, 0.3750, 0.5000])
    
    xm  = np.array([cp1[0], cp2[0], cp3[0], cp4[0]])
    ym  = np.array([cp1[1], cp2[1], cp3[1], cp4[1]])
    x1n = np.array([n1[0],  n2[0],  n3[0],  n4[0]])
    y1n = np.array([n1[1],  n2[1],  n3[1],  n4[1]])
    x2n = np.array([m1[0],  m2[0],  m3[0],  m4[0]])
    y2n = np.array([m1[1],  m2[1],  m3[1],  m4[1]])
    
    # print the tabulated data
    panel = ['1', '2', '3', '4']
    cp = [cp1, cp2, cp3, cp4]
    n = [n1, n2, n3, n4]
    m = [m1, m2, m3, m4]
    print('%-10s %-10s %-10s %-10s %-10s %-10s %-10s' 
              %('Panel', 'xm', 'ym', 'x1n', 'y1n', 'x2n', 'y2n'))
    for i in range(4):
        print('%-10s %-10s %-10s %-10s %-10s %-10s %-10s' 
                  %(panel[i], round(cp[i][0], 4), round(cp[i][1], 4), 
                    round(n[i][0], 4), round(n[i][1], 4), round(m[i][0], 4), 
                    round(m[i][1], 4)))
        
    i = 0
    w1 = []
    w2 = []
    w3 = []
    w4 = []
    for i in range(4):
        for j in range(4):
            sol1 = [wmn(xm[i], x1n[j], x2n[j], ym[i],  y1n[j],  y2n[j])]
            sol2 = [wmn(xm[i], x1n[j], x2n[j], ym[i], -y1n[j], -y2n[j])]
            if i == 0:
                w1.append(sol1[0] - sol2[0])
            elif i == 1:
                w2.append(sol1[0] - sol2[0])
            elif i == 2:
                w3.append(sol1[0] - sol2[0])
            elif i == 3:
                w4.append(sol1[0] - sol2[0])
    
    A = np.array([w1, w2, w3, w4])
    B = np.array([-1, -1, -1, -1])
    sol = np.linalg.solve(A, B)
    deltay = abs(y1n - y2n)
    L = 8*sum(sol*deltay)
    Cl = 10*L
    Cl_alpha = Cl*np.pi
    print('C_L_alpha = {} per radian'.format(Cl_alpha))
        
    
    # # plot the calculated points
    # points = [cp1, cp2, cp3, cp4, n1, n2, n3, n4, m1, m2, m3, m4]
    # x, y = zip(*points)
    # x = list(x)
    # y = list(y)
    # plt.scatter(x, y)
    # annotations = ['CP1', 'CP2', 'CP3', 'CP4']
    # for i, text in enumerate(annotations):
    #     plt.annotate(text, (x[i], y[i]))
    
    # # plot the leading edge
    # LE_points = [(0, 0), (0.5*np.tan(sweep_LE), 0.5)]
    # plot(LE_points)
    
    # # plot the 1/4 chord
    # c14 = [n1, m4]
    # plot(c14)
    
    # # plot the trailing edge
    # point1 = (rc, 0)
    # point2 = (0.5*np.tan(sweep_100)+ rc, 0.5)
    # plot([point1, point2])
    
    # # plot the root chord
    # r_points = [(0, 0), (rc, 0)]
    # plot(r_points)
    
    # # plot the tip chord
    # t_points = [(0.5*np.tan(sweep_LE), 0.5), (0.5*np.tan(sweep_100) + rc, 0.5)]
    # plot(t_points)
    
    # # plot the section dividers
    # l1 = [(n2), ((0.5*np.tan(sweep_100) + rc), n2[1])]
    # plot(l1, 'black')
    
    # l2 = [(n3), ((0.5*np.tan(sweep_100) + rc), n3[1])]
    # plot(l2, 'black')
    
    # l3 = [(n4), ((0.5*np.tan(sweep_100) + rc), n4[1])]
    # plot(l3, 'black')
    
    # plt.legend(['Leading Edge', 'Quarter Chord', 'Trailing Edge', 'Root Chord', 'Tip Chord'])
    # plt.xlabel('x*b')
    # plt.ylabel('y*b')
    # plt.title('AE 422 Project 1')
    
        
        
        