import sys
import math
from random import randint, random


class Schaffer(object):

    def __init__(self, iterations=1000):
        self.max_x = 10 ** 5
        self.min_x = - self.max_x
        self.low, self.high = self.run(iterations)
        self.emax = self.high

    def random_valid_x(self):
        rand_x = float(randint(self.min_x, self.max_x))
        normalized_x = (rand_x - self.min_x) / (self.max_x - self.min_x)
        return normalized_x

    def run(self, iterations):

        low = sys.maxint
        high = - (low + 1)

        for i in range(1, iterations):
            x = self.random_valid_x()

            current_sum = self.sum(x)

            if (current_sum < low):
                low = current_sum

            elif (current_sum > high):
                high = current_sum

        return (low, high)

    def sum(self, x):
        return (x ** 2 + (x - 2) ** 2)

    def energy(self, soln_tuple, normalize=False):

        x, func_sum = soln_tuple

        if normalize:
            return (func_sum - self.low) / (self.high - self.low)

        else:
            return func_sum


class SA(object):

    def __init__(self, kmax=1000, model=None):

        if model is None:
            model = Schaffer()

        self.model = model
        self.kmax = kmax

    def prob(self, old, new, t):
        if t == 0:
            return 0
        return math.e ** ((old - new) / t)

    def run(self):
        """
        s: Tuple (x, f1+f2)
        """
        random_x = self.model.random_valid_x()
        s = (random_x, self.model.sum(random_x))
        e = self.model.energy(s, True)
        sb = s
        eb = e
        k = 0
        emax = 0

        while k < self.kmax and e > emax:
            random_x = self.model.random_valid_x()
            sn = (random_x, self.model.sum(random_x))
            en = self.model.energy(sn, True)
            if (en > 1 or en < 0):
                continue
            # print "*************" + str(en)
            sobriety = (float(k) / self.kmax)
            # print sobriety

            if (k % 50 == 0):
                print ""
                print eb,

            if en < eb:
                sb = sn
                eb = en
                print "!",

            if en < e:
                s = sn
                e = en
                print "+",

            elif self.prob(e, en, sobriety) < random():
                s = sn
                e = en
                print "?",

            else:
                print ".",

            k = k + 1

        return sb, eb


sa = SA(kmax=1000)

res, eb = sa.run()
