# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 04:14:28 2015

@author: nebula
"""

import matplotlib.pyplot as plt
import numpy as np
import math

class SolvePDE():
    LINESTYLE = ['-', ':', '--', '-.']
    PRINT_RANGE = 10

    X  = 1.0
    NX = 101
    DT = 0.1
    NT = 100
    F  = 0.2
    Y0 = 100
    
    def __init__(self):
        self.y0 = [0] * self.NX
        self.y0[self.NX/2] = self.Y0

        self.x = range(self.NX)
        self.result = {}
        
    def __repr__(self):
        return repr(self.result)
        
    def plot(self):
        i = 0
        for k,v in self.result.items():
            plt.plot(self.x, v, linestyle=(self.LINESTYLE[i % len(self.LINESTYLE)]), linewidth=2, label=k)
            i += 1
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend(loc=2)
        plt.show()
        
    def calc_FTCS(self):
        for t in [tmp_t*self.DT for tmp_t in range(self.NT)]:
            for i in range(1, self.NX):
                pass

        self.result['FTCS'] = self.y0

        
if __name__ == '__main__':
    pde = SolvePDE()
    pde.calc_FTCS()
    pde.plot()
    print pde
    
    