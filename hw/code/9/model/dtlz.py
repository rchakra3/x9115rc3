from __future__ import division
from model import Model
from helpers.decision import Decision
import math

PI = math.pi


class DTLZ1(Model):

    def __init__(self, num_decs, num_objs):
        Model.__init__(self)
        self.initialize_decs(num_decs)
        self.num_objs = num_objs

    def initialize_decs(self, num_decs):

        for i in range(num_decs):
            dec = Decision('x' + str(i + 1), 0, 1)
            self.decs.append(dec)

    def eval(self, candidate):
        num_objs = self.num_objs
        dec_vals = candidate.dec_vals
        num_decs = len(dec_vals)

        objectives = [0 for _ in range(self.num_objs)]

        def g():
            val = 0
            for i in range(num_decs):
                val += math.pow(dec_vals[i] - 0.5, 2) - math.cos(20 * PI * (dec_vals[i] - 0.5))
            val = 100 * (val + num_decs)
            return val

        g_val = g()

        objectives[0] = 0.5 * (1 + g_val)

        for i in range(0, num_objs - 1):
            objectives[0] *= dec_vals[i]

        # print objectives[0]

        for i in range(1, num_objs - 1):
            objectives[i] = 0.5 * (1 + g_val)
            for j in range(num_objs - (i + 1)):
                objectives[i] *= dec_vals[j]
            objectives[i] *= 1 - dec_vals[num_objs - (i + 1)]

        objectives[num_objs - 1] = 0.5 * (1 - dec_vals[0]) * (1 + g_val)

        # print objectives
        # print len(objectives)
        # print objectives
        candidate.scores = objectives


class DTLZ3(Model):

    def __init__(self, num_decs, num_objs):
        Model.__init__(self)
        self.initialize_decs(num_decs)
        self.num_objs = num_objs

    def initialize_decs(self, num_decs):

        for i in range(num_decs):
            dec = Decision('x' + str(i + 1), 0, 1)
            self.decs.append(dec)

    def eval(self, candidate):
        num_objs = self.num_objs
        dec_vals = candidate.dec_vals
        num_decs = len(dec_vals)

        objectives = [0 for _ in range(num_objs)]
        num_decs = len(dec_vals)

        def g():
            val = 0
            for i in range(num_decs):
                val += math.pow(dec_vals[i] - 0.5, 2) - math.cos(20 * PI * (dec_vals[i] - 0.5))
            val = 100 * (val + num_decs)
            return val

        g_val = g()
        objectives[0] = 1 + g_val
        for i in range(0, num_objs - 1):
            objectives[0] *= math.cos(dec_vals[i] * PI / 2)

        for i in range(1, num_objs - 1):
            objectives[i] = 1 + g_val
            for j in range(0, num_objs - (i + 1)):
                objectives[i] *= math.cos(dec_vals[j] * PI / 2)
            objectives[i] *= math.sin(dec_vals[num_objs - (i + 1)] * PI / 2)

        objectives[num_objs - 1] = (1 + g_val) * math.sin(dec_vals[0] * PI / 2)

        candidate.scores = objectives


class DTLZ5(Model):

    def __init__(self, num_decs, num_objs):
        Model.__init__(self)
        self.initialize_decs(num_decs)
        self.num_objs = num_objs

    def initialize_decs(self, num_decs):

        for i in range(num_decs):
            dec = Decision('x' + str(i + 1), 0, 1)
            self.decs.append(dec)

    def eval(self, candidate):
        num_objs = self.num_objs
        dec_vals = candidate.dec_vals
        num_decs = len(dec_vals)

        theta = [0 for _ in range(num_objs)]
        objectives = [0 for _ in range(num_objs)]
        num_decs = len(dec_vals)

        def g():
            val = 0
            for i in range(num_decs):
                val += math.pow(dec_vals[i] - 0.5, 2)

            return val

        g_val = g()
        t = 0
        theta[0] = dec_vals[0]
        t = 1 / (2 * (1 + g_val))

        for i in range(1, num_objs):
            theta[i] = t + ((g_val * dec_vals[i]) / (1 + g_val))

        objectives[0] = 1 + g_val
        for i in range(num_objs - 1):
            objectives[0] *= math.cos(theta[i] * PI / 2)

        for i in range(1, num_objs - 1):
            objectives[i] = 1 + g_val
            for j in range(num_objs - (i + 1)):
                objectives[i] *= math.cos(theta[j] * PI / 2)
            objectives[i] *= math.sin(theta[num_objs - (i + 1)] * PI / 2)

        objectives[num_objs - 1] = (1 + g_val) * math.sin(theta[0] * PI / 2)

        candidate.scores = objectives


class DTLZ7(Model):

    def __init__(self, num_decs, num_objs):
        Model.__init__(self)
        self.initialize_decs(num_decs)
        self.num_objs = num_objs

    def initialize_decs(self, num_decs):

        for i in range(num_decs):
            dec = Decision('x' + str(i + 1), 0, 1)
            self.decs.append(dec)

    def eval(self, candidate):
        num_objs = self.num_objs
        dec_vals = candidate.dec_vals
        num_decs = len(dec_vals)

        objectives = [0 for _ in range(num_objs)]
        num_decs = len(dec_vals)

        def g():
            val = sum(dec_vals)
            return 1 + (9 * val / num_decs)

        def h(objectives, g_val):
            val = 0
            for i in range(0, num_objs - 1):
                val += (objectives[i] / (1 + g_val)) * (1 + math.sin(3 * PI * objectives[i]))
            return num_objs - val

        g_val = g()

        for i in range(0, num_objs - 1):
            objectives[i] = dec_vals[i]

        objectives[num_objs - 1] = (1 + g_val) * h(objectives, g_val)

        # print objectives

        candidate.scores = objectives
