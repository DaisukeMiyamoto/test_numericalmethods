# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 01:29:38 2015

@author: nebula
"""
import math
import matplotlib.pyplot as plt

class HodgkinHuxley():
    LINESTYLE = ['-', ':', '--', '-.']
    I_INJ = 10 # [nA]

    def __init__(self):
        self.table = {}
        self.table_max_v = 100.0
        self.table_min_v = -100.0
        self.table_size = 201
        self.i_inj = []
        
        self.makeTable()
    
    def _vtrap(self, x, y):
        x = float(x)
        y = float(y)
        if math.fabs(x / y) > 1e-6:
            return x / (math.exp(x/y) - 1.0)
        else:
            return y * (1.0 - x/y/2.)
            
    def _alpha_n(self, v):
        return 0.01 * self._vtrap(-(v+55.), 10.)

    def _beta_n(self, v):
        return 0.125 * exp(-(v+65.) / 80.)

    def _alpha_m(self, v):
        return 0.1 * self._vtrap(-(v+40.), 10.)
        
    def _beta_m(self, v):
        return 4.  * math.exp(-(v+65.) / 18.)

    def _alpha_h(self, v):
        return 0.07 * math.exp(-(v+65.) / 20.)

    def _beta_h(self, v):
        return 1.0 / (exp(-(v+35.)/10.) + 1.0)
        
    def _i2v(self, i):
        return (self.table_max_v - self.table_min_v) / (self.table_size -1) * float(i) + self.table_min_v


    def makeTable(self):
        self.table['n_tau'] = []
        self.table['n_inf'] = []
        self.table['m_tau'] = []
        self.table['m_inf'] = []
        self.table['h_tau'] = []
        self.table['h_inf'] = []

        for i in range(self.table_size):
            v = self._i2v(i)
            a_n = self._alpha_n(v)
            b_n = self._beta_n(v)
            a_m = self._alpha_m(v)
            b_m = self._beta_m(v)
            a_h = self._alpha_h(v)
            b_h = self._beta_h(v)
            self.table['n_tau'].append(1.0 / (a_n + b_n))
            self.table['n_inf'].append(a_n / (a_n + b_n))
            self.table['m_tau'].append(1.0 / (a_m + b_m))
            self.table['m_inf'].append(a_m / (a_m + b_m))
            self.table['h_tau'].append(1.0 / (a_h + b_h))
            self.table['h_inf'].append(a_h / (a_h + b_h))
            
    def plotDict(self, dct):
        i = 0
        rng = [self._i2v(tmp_i) for tmp_i in range(self.table_size)]
        for k,v in dct.items():
            plt.plot(rng, v, linestyle=(self.LINESTYLE[i % len(self.LINESTYLE)]), linewidth=2, label=k)
            i += 1    
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend(loc=2)
        plt.show()
        
    
    def showTable(self):
        st = '     V     :'
        for k in self.table.keys():
            for i in range(12 - len(k)):
                st += '-'
            st += k + '-'
        st += '\n'
        for i in range(0, self.table_size, 10):
            st += '%10.4f :' % self._i2v(float(i))
            for val in self.table.values():
                st += ' %12.8f' % val[i]
            st += '\n'
        print st

    def _i_inj(self, t):
        if t > 50 and t < 350:
            return self.I_INJ
         
    def _v2i(self, v):
        i = int(v - self.table_min_v)
        theta = (v - self.table_min_v) - float(i)
        if(i >= self.table_size-1):
            i = self.table_size-1
            theta = 1.0
        if(i < 0):
            i = 0
            theta = 0.0
        
        return i, theta
         
    def calc_n(self, v, n): 
        table = self.table
        i, theta = self._v2i(v)

        n_tau = table['n_tau'][i] + theta * (table['n_tau'][i+1] - table['n_tau'][i])
        n_inf = table['n_inf'][i] + theta * (table['n_inf'][i+1] - table['n_inf'][i])

        n += (1.0 - math.exp(-self.DT/n_tau)) * (n_inf - n)
        self.n = n
        return n

    def calc_m(self, v, m): 
        table = self.table
        i, theta = self._v2i(v)

        m_tau = table['m_tau'][i] + theta * (table['m_tau'][i+1] - table['m_tau'][i])
        m_inf = table['m_inf'][i] + theta * (table['m_inf'][i+1] - table['m_inf'][i])

        m += (1.0 - math.exp(-self.DT/m_tau)) * (m_inf - m)
        self.m = m
        return m

    def calc_h(self, v, h): 
        table = self.table
        i, theta = self._v2i(v)

        h_tau = table['h_tau'][i] + theta * (table['h_tau'][i+1] - table['h_tau'][i])
        h_inf = table['h_inf'][i] + theta * (table['h_inf'][i+1] - table['h_inf'][i])

        h += (1.0 - math.exp(-self.DT/h_tau)) * (h_inf - h)
        self.h = h
        return h

if __name__ == '__main__':
    hh = HodgkinHuxley()
    hh.showTable()
    hh.plotDict(hh.table)
