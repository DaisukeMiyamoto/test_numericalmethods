# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 21:39:30 2015

@author: nebula
"""

import matplotlib.pyplot as plt
import numpy as np


def main():
    h = 0.1
    x0 = 0.0
    y0 = 1.0
    n = 109
    y = {}
    

    for i in range(0, n, 10):
        print '%10.4f :' % x[i] ,
        for tmp_y in y.values():
            print ' %10.4f' % tmp_y[i] ,
        #print '%10.4f : %10.4f %10.4f %10.4f' % (x[i], y['euler'][i], y['heun'][i], y['rk4'][i])
        print ''



    linestyle = ['-', ':', '--']

    for i, tmp_y in enumerate(y.values()):
        plt.plot(x, tmp_y)
        #plt.plot(x, tmp_y, linestyle=(linestyle[i % len(linestyle)]))
    plt.show()

if __name__ == '__main__':
    main()
    

