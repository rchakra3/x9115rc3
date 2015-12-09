from __future__ import division
from model import Model
from helpers.decision import Decision
import math


class DTLZ7(Model):

    def __init__(self):
        Model.__init__(self)
        self.initialize_decs()

    def initialize_decs(self):
        dec = Decision('x1', 0, 1)
        self.decs.append(dec)
        dec = Decision('x2', 0, 1)
        self.decs.append(dec)
        dec = Decision('x3', 0, 1)
        self.decs.append(dec)
        dec = Decision('x4', 0, 1)
        self.decs.append(dec)
        dec = Decision('x5', 0, 1)
        self.decs.append(dec)
        dec = Decision('x6', 0, 1)
        self.decs.append(dec)
        dec = Decision('x7', 0, 1)
        self.decs.append(dec)
        dec = Decision('x8', 0, 1)
        self.decs.append(dec)
        dec = Decision('x9', 0, 1)
        self.decs.append(dec)
        dec = Decision('x10', 0, 1)
        self.decs.append(dec)

    def f1(self, candidate):
        val = candidate.dec_vals[0]
        # print "f1:"+str(val)
        return val

    def f2(self, candidate):
        f1_val = self.f1(candidate)
        g_val = self.g(candidate.dec_vals)
        f2 = (1 + g_val) * self.h(f1_val, g_val, 2)
        # print "f2:" + str(f2)
        # print "*************"
        # print g_val
        # print f1_val
        # print f2
        return f2

    def g(self, x):
        val = sum(x)
        # print res
        val = 1 + (9 / len(x)) * val
        # print res
        return val

    def h(self, f1_val, g_val, num_obj):
        val = (f1_val / (1 + g_val)) * (1 + math.sin(3 * math.pi * f1_val))
        val = num_obj - val
        return val

    def objectives(self):
        return [self.f1, self.f2]

    def aggregate(self, candidate):
        aggr = 0
        self.eval(candidate)
        for score in candidate.scores:
            aggr += score
        return aggr
