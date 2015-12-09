class Candidate(object):

    def __init__(self, dec_vals=None, scores=None):

        if dec_vals is None:
            dec_vals = []
        if scores is None:
            scores = []
        self.dec_vals = []
        self.scores = []
        for dec_val in dec_vals:
            self.dec_vals += [dec_val]
        for score in scores:
            self.scores += [score]

    def add_dec(self, val):
        self.dec_vals.push(val)

    def add_scores(self, val):
        self.scores.push(val)
