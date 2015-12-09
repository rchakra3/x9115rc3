from model import Model
from helpers.decision import Decision
import math


class Kursawe(Model):

    def __init__(self):
        Model.__init__(self)
        self.initialize_decs()

    def initialize_decs(self):
        dec = Decision('x1', -5, 5)
        self.decs.append(dec)
        dec = Decision('x2', -5, 5)
        self.decs.append(dec)
        dec = Decision('x3', -5, 5)
        self.decs.append(dec)

    def f1(self, candidate):
        vec = candidate.dec_vals
        n = len(vec)
        sum = 0

        for i in range(n - 1):
            sum += (-10 * math.exp(-0.2 * math.sqrt(vec[i] ** 2 + vec[i + 1] ** 2)))

        return sum

    def f2(self, candidate):
        vec = candidate.dec_vals
        n = len(vec)
        sum = 0

        for i in range(n):
            sum += (abs(vec[i]) ** 0.8 + 5 * math.sin(vec[i]))

        return sum

    def objectives(self):
        return [self.f1, self.f2]

    def aggregate(self, candidate):
        aggr = 0
        self.eval(candidate)
        for score in candidate.scores:
            aggr += score
        return aggr
