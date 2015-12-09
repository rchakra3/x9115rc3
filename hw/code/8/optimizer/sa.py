from __future__ import division
import random
from common import prerun
from model.helpers.candidate import Candidate
from helpers.sk import a12
# from helpers.sk import r
from helpers.cdom import cdom
import math
import sys


def sa_default_prob(curr_score, new_score, t):
    # if t == 0:
    #     return 0
    try:
        val = math.exp((curr_score - new_score) / t)
    except:
        val = 1
    # print val
    return val


def sa(model, p=sa_default_prob, threshold=0.001, max_tries=100000, lives=10, era_size=2000, era0=None):

    normalize = prerun(model)

    aggregate = model.aggregate

    def actual_n_score(can):
        return normalize(aggregate(can))

    def n_score(can):
        return aggregate(can)
        # return normalize(aggregate(can))

    # if energy of can1 is less than that of can2
    # can1 is better and this returns true
    def type1(can1, can2):
        # res = cdom(can1.dec_vals, can2.dec_vals)
        # # print "*************************************"
        # # print res
        # # print "*************************************"
        # if res == can1.dec_vals:
        #     # print "TrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrueTrue"
        #     return True
        # else:
        #     return False
        return (n_score(can1) < n_score(can2))

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

    # One era is a list of size era_size
    # Each element is a list with all the values of an objective in that era
    # So basically: era = [[can1.obj1_score, can2.obj1_score],
    #                      [can1.obj2.score, can2.obj2.score]]

    if not era0:
        best_can = model.gen_candidate()
        while best_can is None:
            best_can = model.gen_candidate()

        best_score = n_score(best_can)
        curr_can = best_can
        curr_score = best_score
        curr_era = [[] for _ in model.objectives()]

    else:
        # List of List. Need to deepcopy internal list too
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
        for can in era0_copy:
            if type1(can, best_can):
                best_can = can
        curr_can = era0_copy[len(era0_copy) - 1]
        curr_score = n_score(curr_can)

    best_score = n_score(best_can)

    out = []

    eras = []
    curr_lives = lives
    i = -1

    # If in `lives` eras there is no improvement, EXIT
    # If iterations > max_tries, EXIT
    # If n_score <threshold, EXIT

    gen_count = 0
    none_count = 0

    early_termination = False

    random_jumps = 0
    gt_50 = 0

    while True:
        i += 1

        if i == max_tries:
            out += ["\nReached max tries"]
            if curr_era:
                eras += [curr_era]
                curr_era = [[] for _ in model.objectives()]
            break

        # Beginning of a new ERA
        if i % era_size == 0:
            # print "Random Jumps this era:" + str(random_jumps)
            # print "gt_50 this era:" + str(gt_50)
            gt_50 = 0
            random_jumps = 0
            out += ["\n" + str(best_score) + " "]
            if curr_era:
                eras += [curr_era]
                curr_era = [[] for _ in model.objectives()]
                if len(eras) > 1:
                    last_index = len(eras) - 1
                    # If there is improvement reset lives, else decrement
                    if (type2(eras[last_index - 1], eras[last_index])):
                        curr_lives += lives
                    else:
                        curr_lives -= 1
                        if curr_lives == 0:
                            print "No more lives"
                            out += ["\nNo more Lives"]
                            early_termination = True
                            break

        new_can = model.gen_candidate()
        # new_can = model.gen_can_from_prev(curr_can)

        gen_count += 1
        if new_can is None:
            none_count += 1
            out += ["."]
            model.eval(curr_can)
            obj_scores = [x for x in curr_can.scores]
            for index, score in enumerate(obj_scores):
                curr_era[index] += [score]
            continue

        model.eval(new_can)
        obj_scores = [x for x in new_can.scores]
        for index, score in enumerate(obj_scores):
                curr_era[index] += [score]

        new_score = n_score(new_can)

        flag = True
        # if new_score < best_score:
        if type1(new_can, best_can):
            best_score = new_score
            best_can = new_can
            # print "!"
            out += ["!"]
            flag = False

        # if new_score < curr_score:
        norm_curr_score = actual_n_score(curr_can)
        norm_new_score = actual_n_score(new_can)
        prob = p(norm_curr_score, norm_new_score, ((i / max_tries)))
        # print "****************************"
        # print (norm_curr_score - norm_new_score)
        # print (i/max_tries)
        if(prob>0.5):
            gt_50 += 1
            # print str(prob)
        if type1(new_can, curr_can):
            # print "new can won"
            curr_score = new_score
            curr_can = new_can
            out += ["+"]
            flag = False

        elif prob < random.random():
            # print "random jump"
            curr_score = new_score
            curr_can = new_can
            out += ["?"]
            random_jumps += 1
            flag = False

        # else:
        #     print "_!_"

        if best_score < threshold:
            early_termination = True
            out += ["\nScore satisfies Threshold"]
            break

        if flag is True:
            out += "."

    if curr_era:
        eras += [curr_era]

    # for era in eras:
    #     print era
    #     print "******"
        # break
    # print eras[len(eras) - 2]

    # print len(eras[0])
    # print len(eras[len(eras) - 2])

    # print ''.join(out)
    # print "gen_count:" + str(gen_count)
    # print "none_count" + str(none_count)
    # print "\nLen (eras):" + str(len(eras))
    # print "\niterations:" + str(i)
    # print "Score:" + str(best_score)
    return best_can, best_score, eras[len(eras) - 2]
