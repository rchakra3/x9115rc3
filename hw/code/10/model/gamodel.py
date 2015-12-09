from __future__ import division
from model import Model
from helpers.decision import Decision
import math

PI = math.pi


class GAModel(Model):

    def __init__(self, num_decs, num_objs, ga_func, model_instance, initial_pop=None):
        Model.__init__(self)
        self.initialize_decs(num_decs)
        self.num_objs = num_objs
        self.ga_func = ga_func
        self.model_instance = model_instance
        self.initial_pop = initial_pop

    def initialize_decs(self, num_decs):

        dec = Decision('mutation_prob', 0, 1)
        self.decs.append(dec)
        # number of crossover points
        dec = Decision('cop', 1, 5, type="int")
        self.decs.append(dec)
        # population size
        dec = Decision('pop_size', 50, 150, type="int")
        self.decs.append(dec)

    def eval(self, candidate):

        mutation_prob = candidate.dec_vals[0]
        cop = int(candidate.dec_vals[1])
        # print "cop:" + str(cop)
        pop_size = int(candidate.dec_vals[2])

        score = self.ga_func(self.model_instance, mp=mutation_prob, cop=cop, population_size=pop_size, initial_pop=self.initial_pop)

        # print objectives
        # print len(objectives)
        # print objectives
        print 1 - score
        candidate.scores = [1 - score]

    def objectives(self):
        return [None]
