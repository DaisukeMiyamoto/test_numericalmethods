# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 01:29:38 2015

@author: nebula
"""
import math
import matplotlib.pyplot as plt

class HodgkinHuxley():
    LINESTYLE = ['-', ':', '--', '-.']
    I_INJ = 5    # [nA]
    DT    = 0.025 # [msec]

    def __init__(self):
        self.table = {}
        self.table_max_v = 100.0
        self.table_min_v = -100.0
        self.table_size = 201
        self.i_inj = []
        self.cm      =   1.0 # [muF/cm^2]
        self.e_k     = -77.0 # [mV]
        self.e_na    =  50.0 # [mV]
        self.gk_max  =  36.0 # [mS/cm^2]
        self.gna_max = 120.0 # [mS/cm^2]
        self.gm      =   0.3 # [mS/cm^3]
        self.v_rest  = -54.3 # [mV]
        self.v       = -65.0 # [mV]
        self.n = self._alpha_n(self.v) / (self._alpha_n(self.v) + self._beta_n(self.v))
        self.m = self._alpha_m(self.v) / (self._alpha_m(self.v) + self._beta_m(self.v))
        self.h = self._alpha_h(self.v) / (self._alpha_h(self.v) + self._beta_h(self.v))
        
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
        plt.xlabel('V [mV]')
        plt.ylabel('Y')
        plt.legend()
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

    def _i_inj(self):
        t = self.t
        if t > 5:
            return self.I_INJ
        else:
            return 0.0
         
    def _v2i(self, v):
        i = int(v - self.table_min_v)
        theta = (v - self.table_min_v) - float(i)
        if(i >= self.table_size-2):
            i = self.table_size-2
            theta = 1.0
        if(i < 0):
            i = 0
            theta = 0.0
        #print i,theta
        
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
        
    def calc_v(self, v, n, m, h):
        v += self.DT / self.cm \
        * (self.gk_max * (n**4) * (self.e_k - v) \
        + self.gna_max * (m**3) * h * (self.e_na - v) \
        + self.gm * (self.v_rest - v) + self._i_inj())
        self.v = v
        return v

if __name__ == '__main__':
    hh = HodgkinHuxley()
    hh.showTable()
    hh.plotDict(hh.table)

    record = {}
    record['t'] = [0]
    record['v'] = [hh.v]
    record['n'] = [hh.n]
    record['m'] = [hh.m]
    record['h'] = [hh.h]
    for i in range(1000):
        record['t'].append(record['t'][-1] + hh.DT)
        hh.t = record['t'][-1]
        record['n'].append(hh.calc_n(record['v'][-1], record['n'][-1]))
        record['m'].append(hh.calc_m(record['v'][-1], record['m'][-1]))
        record['h'].append(hh.calc_h(record['v'][-1], record['h'][-1]))
        record['v'].append(hh.calc_v(record['v'][-1], record['n'][-1], record['m'][-1], record['h'][-1]))
        
        
    plt.plot(record['t'], record['v'])
    plt.ylim(-80, 80)
    plt.xlabel('t [msec]')
    plt.ylabel('V [mV]')
    plt.show()

    plt.plot(record['t'], record['m'], label='m')
    plt.plot(record['t'], record['h'], label='h')
    plt.plot(record['t'], record['n'], label='n')
    n4 = [n**4 for n in record['n']]
    m3h = [m**3*h for m,h in zip(record['m'], record['h'])]
    plt.plot(record['t'], m3h, label='m^3 * h')
    plt.plot(record['t'], n4, label='n^4')
    plt.legend(loc=1)
    plt.xlabel('t [msec]')
    plt.show()
    
    #plt.legend(loc=1)
    #plt.xlabel('t [msec]')
    #plt.show()

