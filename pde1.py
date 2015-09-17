# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 04:14:28 2015

@author: nebula
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

class SolvePDE():
    LINESTYLE = ['-', ':', '--', '-.']
    PRINT_RANGE = 10

    X  = 1.0
    NX = 101
    DT = 0.1
    NT = 200
    F  = 0.1
    Y0 = 100
    
    def __init__(self):
        self.y0 = [0] * self.NX
        self.y0[self.NX/2] = self.Y0
        self.t = [tmp_t*self.DT for tmp_t in range(self.NT)]
        self.x = range(self.NX)
        self.result = {}
        
    def __repr__(self):
        return repr(self.result)
        
    def plot(self):
        #i = 0
        xx,tt = (np.mat(A) for A in (np.meshgrid(self.x, self.t)))
        fig = plt.figure()
        ax = Axes3D(fig)
        for k,v in self.result.items():
            #plt.plot(self.x, v[0], linestyle=(self.LINESTYLE[i % len(self.LINESTYLE)]), linewidth=2, label=k)
            #i += 1
            ax.plot_wireframe(xx, tt, v, rstride=5, cstride=5, label=k)

        plt.xlabel('X')
        plt.ylabel('T [msec]')
        plt.ylabel('Y')
        plt.legend(loc=2)
        plt.show()
        
    def calc_FTCS(self):
        y = [self.y0]
        for t in self.t[1:]:
            tmp_y = [0]
            for i in range(1, self.NX-1):                
                tmp_y.append(y[-1][i] + self.F * (y[-1][i-1] - 2*y[-1][i] + y[-1][i+1]))
            tmp_y.append(0)
            y.append(tmp_y)

            #u[i] = u_1[i] + F*(u_1[i-1] - 2*u_1[i] + u_1[i+1])

        self.result['FTCS'] = y

        
if __name__ == '__main__':
    pde = SolvePDE()
    pde.calc_FTCS()
    pde.plot()
    #print pde
    
    