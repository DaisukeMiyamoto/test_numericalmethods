# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 21:39:30 2015

@author: nebula
"""

import matplotlib.pyplot as plt
import numpy as np
import math

class SolveODE():
    LINESTYLE = ['-', ':', '--', '-.']
    PRINT_RANGE = 10

    def __init__(self, func=None, x0=0.0, y0=1.0, h=0.1, n=100):
        self.x0 = x0
        self.y0 = y0
        self.n  = n
        self.h  = h
        self.result = {}
        
        self.x = [self.x0]
        for i in range(self.n):
            self.x.append(self.x[-1] + self.h)

        if func is None:
            self.f = self._func
        else:
            self.f = func

    def _func(self, x, y):
        return x + y

    def __str__(self):
        st = '     X     :'
        for k in self.result.keys():
            for i in range(12 - len(k)):
                st += '-'
            st += k + '-'
        st += '\n'
        for i in range(0, self.n, self.PRINT_RANGE):
            st += '%10.4f :' % self.x[i]
            for tmp_result in self.result.values():
                st += ' %12.4f' % tmp_result[i]
            st += '\n'
        return st
        
    def __repr__(self):
        return repr(self.result)
        
    def show_plots(self):
        i = 0
        for k,v in self.result.items():
            plt.plot(self.x, v, linestyle=(self.LINESTYLE[i % len(self.LINESTYLE)]), linewidth=2, label=k)
            i += 1    
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend(loc=2)
        plt.show()
        
    def calc_all(self):
        self.calc_euler()
        self.calc_heun()
        self.calc_rk4()
        
    def calc_euler(self):
        f = self.f
        h = self.h
        x = self.x
        y = [self.y0]
        for i in xrange(self.n):
            y.append(y[-1] + h * f(x[i], y[-1]))
            
        self.result['Euler'] = y
        return y
        
    def calc_heun(self):
        f = self.f
        h = self.h
        x = self.x
        y = [self.y0]
        for i in xrange(self.n):
            k1 = f(x[i], y[-1])
            k2 = f(x[i], y[-1]+h*k1)
            y.append(y[-1] + h / 2.0 * (k1 + k2))
        
        self.result['Heun'] = y
        return y
        
    def calc_rk4(self):
        f = self.f
        h = self.h
        x = self.x
        y = [self.y0]
        for i in xrange(self.n):
            k1 = f(x[i],           y[-1])
            k2 = f(x[i] + h / 2.0, y[-1] + h*k1/2.0)
            k3 = f(x[i] + h / 2.0, y[-1] + h*k2/2.0)
            k4 = f(x[i] + h,       y[-1] + h*k3)
            y.append(y[-1] + h / 6.0 * (k1 + 2.0*k2 + 2.0*k3 + k4))
        self.result['RK4'] = y

if __name__ == '__main__':
    def func0(x, y):
        return x - y

    def func0(x, y):
        return x
    
    #solve = SolveODE(func)
    solve = SolveODE()
    solve.calc_all()
    print solve
    solve.show_plots()
    

