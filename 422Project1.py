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
    l1 = 0.75*0.2
    x1 = y*np.tan(sweep) + l1
    return (x1, y)

def coord(y, sweep):
    l1 = 0.25*0.2
    x1 = y*np.tan(sweep) + l1
    return (x1, y)

def plot(lst, color = None):
    x, y = zip(*lst)
    plt.plot(x, y, c = color)
 

if __name__ == '__main__':
    
    # sweep angle at the 1/4 chord
    sweep_25 = 45*(np.pi/180)
    # taper ratio
    lam = 0.5
    # aspect ratio
    AR = 5
    
    # distance between the panels
    x = 0.125
    # distance to the panel mid point
    x1 = x/2
    
    # sweep angle at the leading edge
    sweep_LE  = sweep_LE(0.25, AR, lam, sweep_25)
    # sweep angle at the 3/4 chord
    sweep_75  = sweep(0.75, AR, lam, sweep_LE)
    # sweep angle at the trailing edge
    sweep_100  = sweep(1.0, AR, lam, sweep_LE)
    
    
    # these are all off by 0.05?
    cp1 = cp(x1,       sweep_75)
    cp2 = cp(x1 + x,   sweep_75)
    cp3 = cp(x1 + x*2, sweep_75)
    cp4 = cp(x1 + x*3, sweep_75)
    
    
    # these are all off by 0.016666667?
    n1  = coord(0,     sweep_25)
    n2  = coord(x,     sweep_25)
    n3  = coord(x*2,   sweep_25)
    n4  = coord(x*3,   sweep_25)
    
    m1  = coord(x,     sweep_25)
    m2  = coord(x*2,   sweep_25)
    m3  = coord(x*3,   sweep_25)
    m4  = coord(x*4,   sweep_25)
    
    
    # plot the calculated points
    points = [cp1, cp2, cp3, cp4, n1, n2, n3, n4, m1, m2, m3, m4]
    x, y = zip(*points)
    x = list(x)
    y = list(y)
    plt.scatter(x, y)
    annotations = ['CP1', 'CP2', 'CP3', 'CP4']
    for i, text in enumerate(annotations):
        plt.annotate(text, (x[i], y[i]))
    
    # plot the leading edge
    LE_points = [(0, 0), (0.5*np.tan(sweep_LE), 0.5)]
    plot(LE_points)
    
    # plot the 1/4 chord
    c14 = [n1, m4]
    plot(c14)
    
    # plot the trailing edge
    point1 = (0.2, 0)
    point2 = (0.5*np.tan(sweep_100)+ 0.2, 0.5)
    plot([point1, point2])
    
    # plot the root chord
    r_points = [(0, 0), (0.2, 0)]
    plot(r_points)
    
    # plot the tip chord
    t_points = [(0.5*np.tan(sweep_LE), 0.5), (0.5*np.tan(sweep_100) + 0.2, 0.5)]
    plot(t_points)
    
    # plot the section dividers
    l1 = [(n2), ((0.5*np.tan(sweep_100) + 0.2), n2[1])]
    plot(l1, 'black')
    
    l2 = [(n3), ((0.5*np.tan(sweep_100) + 0.2), n3[1])]
    plot(l2, 'black')
    
    l3 = [(n4), ((0.5*np.tan(sweep_100) + 0.2), n4[1])]
    plot(l3, 'black')
    
    plt.legend(['Leading Edge', 'Quarter Chord', 'Trailing Edge', 'Root Chord', 'Tip Chord'])
    
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
        
        
        