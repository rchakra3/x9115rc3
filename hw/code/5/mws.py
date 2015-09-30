import sys
from copy import copy
from osyczka2 import Osyczka2Solution
from random import randint, random


class MaxWalkSat(object):

    def run_tries(self, threshold=2, max_tries=1000, max_changes=50):
        soln = Osyczka2Solution()
        p = 0.5
        soln.generate_rand_vec()
        best_soln = soln
        best_score = self.score_func(best_soln)

        for i in range(0, max_tries):
            # print "Try:%d" % (i)

            if (i % 10 == 0):
                print "\n",
                print best_score,

            for j in range(0, max_changes):

                if self.score_func(soln) > threshold:
                    evaluations = max_changes * (i - 1)
                    evaluations += j
                    return (evaluations, True, soln)

                if self.score_func(soln) > best_score:
                    print "!",
                    best_soln = copy(soln)
                    best_score = self.score_func(soln)

                c = randint(0, 5)

                if p < random():
                    print "?",
                    soln.random_mutate_element(c)
                else:
                    orig_val = soln.vector[c]
                    soln.maximize_score(c, self.score_func)
                    new_val = soln.vector[c]
                    if new_val == orig_val:
                        print ".",
                    else:
                        print "+",

            soln.generate_rand_vec()

        return (max_changes * max_tries, False, best_soln)

    def mock_run(self, iterations=1000):

        min_val = sys.maxint
        max_val = - min_val - 1

        soln = Osyczka2Solution()

        for i in range(1, iterations):
            soln.generate_rand_vec()
            val = soln.f1() + soln.f2()

            if val > max_val:
                max_val = val

            elif val < min_val:
                min_val = val

        self.min_val = min_val
        self.max_val = max_val

    def score_func(self, soln):

        energy = soln.f1() + soln.f2()
        return ((energy - self.min_val) / (self.max_val - self.min_val))


mws = MaxWalkSat()

mws.mock_run()
(evaluations, found_best, soln) = mws.run_tries(max_tries=100, max_changes=10)

print "\nEvaluations: %d" % evaluations
# print found_best
print "Best Found: [",
for i, elem in enumerate(soln.vector):
    print str(elem),
    if i is not (len(soln.vector) - 1):
        print ",",
print "]"
