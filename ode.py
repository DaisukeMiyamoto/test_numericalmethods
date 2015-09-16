# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 21:39:30 2015

@author: nebula
"""

import matplotlib.pyplot as plt
import numpy as np

def calc_euler(x0, y0, dt, n , f):
    x = [x0]
    y = [y0]
    for i in range(n):
        y.append(y[-1] + dt * f(x[-1], y[-1]))
        x.append(x[-1] + dt)
        
    return x, y


def func(x, y):
    return x + y

def main():
    h = 0.1
    x0 = 0.0
    y0 = 1.0
    n = 109
    y = {}

    x, y['euler'] = calc_euler(x0, y0, h, n, func)
    

    for i in range(0, n, 10):
        print '%10.4f :' % x[i] ,
        for tmp_y in y.values():
            print ' %10.4f' % tmp_y[i] ,
        print ''



    linestyle = ['-', ':', '--', '-.']
    for k,v in y.items():
        plt.plot(x, y[k], linestyle=(linestyle[i % len(linestyle)]), linewidth=2, label=k)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(loc=2)
    plt.show()

if __name__ == '__main__':
    main()
    

