from helpers.candidate import Candidate
import random


class Model(object):

    def __init__(self, decs=None, objs=None, patience=100):

        if decs is None:
            decs = []
        if objs is None:
            objs = []
        self.decs = decs
        self.objs = objs
        self.patience = patience

    def eval(self, candidate):
        candidate.scores = [f(candidate) for f in self.objectives()]
        # print "scores:" + str(candidate.scores)

    def ok(self, candidate):
        return True

    def decisions(self):
        return self.decs

    def objectives(self):
        return self.objs

    def gen_candidate(self):
        for i in range(0, self.patience):
            decs = [dec.generate_valid_val() for dec in self.decs]
            can = Candidate(dec_vals=list(decs))
            if self.ok(can):
                return can

    def gen_can_from_prev(self, prev_can):

        for i in range(0, self.patience):
            decs = [dec.generate_valid_val() for dec in self.decs]
            can = Candidate(dec_vals=list(decs))
            for i in range(len(decs)):
                if random.random() < 0.25:
                    can.dec_vals[i] = prev_can.dec_vals[i]
            if self.ok(can):
                return can

    def aggregate(self, candidate):
        aggr = 0
        self.eval(candidate)
        for score in candidate.scores:
            aggr += score
        return aggr
