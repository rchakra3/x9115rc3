from __future__ import division
import random
from common import prerun
from model.helpers.candidate import Candidate
from helpers.a12 import a12


def mws(model, p=0.5, threshold=0.001, max_tries=500, max_changes=10, era_size=100, era0=None, lives=5):

    best_can = None

    max_tries = max_tries / max_changes

    normalize = prerun(model)
    aggregate = model.aggregate

    def n_score(can):
        return aggregate(can)
        # return normalize(aggregate(can))

    # if energy of can1 is less than that of can2
    # can1 is better and this returns true
    def type1(can1, can2):
        return (n_score(can1) < n_score(can2))

    # def type2(era1, era2):
    #     # a12 returns times that lst1 is greater than lst2
    #     total = 0
    #     n = 0
    #     for obj_scores1, obj_scores2 in zip(era1, era2):
    #         # If this is 1, that means new one is worse
    #         total += a12(obj_scores1, obj_scores2)
    #         n += 1
    #     return (total / n >= 0.5)
    def type2(era1, era2):
        # a12 returns times that lst1 is greater than lst2
        # total = 0
        # n = 0
        # for obj_scores1, obj_scores2 in zip(era1, era2):
        #     # If this is 1, that means era1 is greater more often
        #     # If minimizing, this means era1 is worse
        #     total += a12(obj_scores1, obj_scores2)
        #     n += 1
        # return (total / n >= 0.5)

        # Currently returns true if even one of the objectives have improved
        # print "here:" + str(len(era2))
        # print "*****#############*************"
        for index, objective in enumerate(era2):
            # print "comparing:\n" + str(era1[index])
            # print "and\n"
            # print str(objective)
            # print "******"
            a12_score = a12(era1[index], objective)
            # print "######"
            # print a12_score
            # print "######"
            if (a12_score >= 0.56):
                # print "######"
                # print objective
                # print era1[index]
                # print a12_score
                # print "######"
                return True
        # print "######"
        # print a12_score
        # print "######"
        return False

    # best_score = 1.0

    if not era0:
        print "ERRRRRRRRRRRRRRRRRRRRRRRRRRRROR"
        curr_era = [[] for _ in model.objectives()]
        curr_lives = lives

    else:
        # List of List. Need to deepcopy internal list too
        curr_lives = lives
        era0_copy = []
        for can in era0:
            new_can = Candidate(dec_vals=can.dec_vals, scores=can.scores)
            era0_copy += [new_can]
        curr_era = [[] for _ in model.objectives()]
        for can in era0_copy:
            model.eval(can)
            obj_scores = [x for x in can.scores]
            for index, score in enumerate(obj_scores):
                curr_era[index] += [score]

        best_can = era0_copy[0]
        best_score = n_score(best_can)
        for can in era0_copy:
            if type1(can, best_can):
                best_can = can
                best_score = n_score(best_can)
        # curr_can = era0_copy[len(era0_copy) - 1]
        # curr_score = n_score(curr_can)

    # This stores a list of era entries, i.e a list of  [list of objective scores for every candidate in the era]
    # Assume one era is 5 candidates
    # One Era entry for a model with 2 objectives: [[0.5,0.5], [0.2,0.3], [0.5,0.5], [0.2,0.3], [0.5,0.5]]
    # All era entries will be stored in eras (Assume 2 eras): [[[0.5,0.5], [0.2,0.3], [0.5,0.5], [0.2,0.3], [0.5,0.5]],
    #                                                         [[0.5,0.5], [0.2,0.3], [0.5,0.5], [0.2,0.3], [0.5,0.5]]]
    eras = []

    out = []

    candidate = None

    i = -1
    thresh_flag = False

    while not thresh_flag:
        # print "New Try"
        i += 1
        j = 0
        if i == max_tries:
            if curr_era:
                eras += [curr_era]
                # curr_era = [[] for _ in model.objectives()]
            # print "Reached max tries"
            out += ["\nReached Max Tries"]
            break

        if (i * max_changes) % era_size == 0:
            out += ["\n" + str(best_score) + " "]
            if curr_era:
                eras += [curr_era]
                # print len(curr_era[0])
                curr_era = [[] for _ in model.objectives()]
                if len(eras) > 1:
                    # print str(i)+":"+str(i*max_changes)+":lives", curr_lives
                    last_index = len(eras) - 1
                    # If there is improvement reset lives, else decrement
                    if (type2(eras[last_index - 1], eras[last_index])):
                        curr_lives += lives
                    else:
                        curr_lives -= 1
                        if curr_lives == 0:
                            # print "No more"
                            out += ["\nNo more Lives"]
                            break

        if candidate is not None:
            prev_candidate = candidate

        if i == 0:
            while candidate is None:
                candidate = model.gen_candidate()
        else:
            candidate = model.gen_candidate()

        # could not generate a valid candidate after patience tries
        if candidate is None:
            out += ["."]
            model.eval(prev_candidate)
            obj_scores = [x for x in prev_candidate.scores]
            for index, score in enumerate(obj_scores):
                curr_era[index] += [score]
            continue

        if best_can is None:
            best_can = candidate
            best_score = n_score(candidate)

        for j in range(0, max_changes):
            model.eval(candidate)
            score = n_score(candidate)
            # print score

            model.eval(candidate)
            obj_scores = [x for x in candidate.scores]
            for index, score in enumerate(obj_scores):
                curr_era[index] += [score]

            if type1(candidate, best_can):  # score < best_score:
                out += ["!"]
                best_can = candidate
                best_score = score

            # if best_score < threshold:
            #     if curr_era:
            #         eras += [curr_era]
            #         curr_era = [[] for _ in model.objectives()]
            #     out += ["\nScore satisfies threshold"]
            #     thresh_flag = True
            #     break

            # choose a random decision
            c = random.randrange(0, len(model.decs))

            if p < random.random():
                # change the decision randomly
                # ensure it is valid
                patience = model.patience
                while(patience > 0):
                    new_can = Candidate(dec_vals=list(candidate.dec_vals))
                    new_can.dec_vals[c] = model.decs[c].generate_valid_val()
                    if model.ok(new_can):
                        candidate = new_can
                        out += ["?"]
                        break
                    patience -= 1
                if patience == 0:
                    out += ["."]

            else:
                orig_score = n_score(candidate)
                candidate = mws_optimize(model, candidate, c, type1)
                new_score = normalize(model.aggregate(candidate))
                if orig_score != new_score:
                    out += ["+"]
                else:
                    out += ["."]

    # print ''.join(out)
    # print "\niterations:" + str(max_changes * i + j)
    # print "Best Score:" + str(normalize(model.aggregate(best_can)))

    # print eras[len(eras)-1]

    return best_can, model.aggregate(best_can), eras[len(eras) - 1]


def mws_optimize(model, candidate, dec_index, type1, tries=50):

    best_can = candidate
    model.eval(best_can)
    best_score = model.aggregate(best_can)

    # print "Started with " + str(best_score)

    for i in range(0, tries):
        new_can = Candidate(dec_vals=list(candidate.dec_vals))
        # This can be changed to use all possible values
        new_can.dec_vals[dec_index] = model.decs[dec_index].generate_valid_val()
        model.eval(new_can)
        score = model.aggregate(new_can)

        # We want to lower score
        if type1(new_can, best_can):
            best_score = score
            best_can = new_can

    return best_can
