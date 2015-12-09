"""

N = population size
P = create parent population by randomly creating N individuals

while not DONE:
    C = create empty child population
    while not enough indivs in C:
        parent1 = select parent ***SELECTION
        parent2 = select parent ***SELECTION
        child1, child2 = crossover(p1,p2)
        mutate child1, child2
        evaluate child1, child2 for fitness
        insert child1, child2 into C
    end while
    P = combine P and C somehow to get N new individuals


mp => Defaults for mutation: at probability 5%
cop=> Defaults for number of crossover points: one point (i.e. pick a random decision, take all dad's decisions up to that point, take alll mum's decisions after that point)
select=> Defaults for select: for all pairs in the population, apply binary domination.
population_size=> Defaults for number of candidates: 100
num_generations=> Defaults for number of generations: 1000 (but have early termination considered every 100 generations)
"""

from __future__ import division
import random
# from common import prerun
from collections import deque
from model.helpers.candidate import Candidate
import time


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap



def ga_select(population, fitness_func, exclude=None):

    if exclude is None:
        exclude = []

    indiv1 = population[random.randint(0, len(population) - 1)]

    while exclude and indiv1 in exclude:
        indiv1 = population[random.randint(0, len(population) - 1)]

    exclude += [indiv1]

    indiv2 = population[random.randint(0, len(population) - 1)]

    while exclude and indiv2 in exclude:
        indiv2 = population[random.randint(0, len(population) - 1)]

    if fitness_func(indiv1, indiv2):
        return indiv1

    else:
        return indiv2


def crossover(indiv1, indiv2, cop):

    cross_points = []

    indiv_list1 = deque([indiv1, indiv2])
    indiv_list2 = deque([indiv2, indiv1])

    for _ in range(cop):
        cross_points += [random.randint(0, len(indiv1.dec_vals))]

    cross_points.sort()
    cross_point_index = 0

    i = 0
    take_one_from = indiv_list1.popleft()
    indiv_list1.append(take_one_from)

    take_two_from = indiv_list2.popleft()
    indiv_list2.append(take_two_from)

    child1 = Candidate(dec_vals=list(indiv1.dec_vals))
    child2 = Candidate(dec_vals=list(indiv1.dec_vals))

    while i < len(indiv1.dec_vals):
        if cross_point_index < len(cross_points) and i == cross_points[cross_point_index]:
            take_one_from = indiv_list1.popleft()
            indiv_list1.append(take_one_from)
            take_two_from = indiv_list2.popleft()
            indiv_list2.append(take_two_from)
            cross_point_index += 1

        child1.dec_vals[i] = take_one_from.dec_vals[i]
        child2.dec_vals[i] = take_two_from.dec_vals[i]
        i += 1

    return (child1, child2)


def mutate(indiv, probability, property_descriptions, ok):

    first_pass = True

    if random.random() <= probability:
        while first_pass or (not ok(indiv)):
            index = random.randint(0, len(property_descriptions) - 1)
            indiv.dec_vals[index] = property_descriptions[index].generate_valid_val()
            first_pass = False


# @timing
def generate_frontier(frontier, parents, type1, obj_mins, obj_maxs):

    # print len(parents)

    # last = []
    # print "New"
    # print len(frontier)
    # print len(parents)
    for can1 in parents:
        flag = True
        for i, score in enumerate(can1.scores):
            if score < obj_mins[i]:
                obj_mins[i] = score
            if score > obj_maxs[i]:
                obj_maxs[i] = score

        for can2 in parents:
            if can1 == can2:
                continue

            # print "Entering type1"
            if not type1(can1, can2):  # and type1(can2, can1):
                # if count > 10:
                # if last == can1.scores:
                #     print str(count) + "::" + str(can2.scores) + "dominates" + str(can1.scores)
                # last = can2.scores
                # print "Failed"
                flag = False
                break

        if flag:
            # print "Flag is True"
            frontier += [can1]

    del_list = []

    # if len(frontier) > 0:
    #     print len(frontier)

    for i, possible_faker in enumerate(frontier):
        is_faker = True
        for can in frontier:
            if type1(possible_faker, can):  # and not type1(can, possible_faker):
                is_faker = False
                # print "Not faker"
                break
            # else:
            #     print str(possible_faker.scores) + "not better than" + str(can.scores)

        if is_faker:
            del_list += [i]
            # print "FAKER"

    final_frontier = []

    for winner in frontier:
        if winner not in del_list:
            final_frontier += [winner]

    return final_frontier


def generate_random_population(model, population_size):
    parents = []
    while len(parents) < population_size:
        indiv = model.gen_candidate()
        if indiv is not None:
            model.eval(indiv)
            parents += [indiv]

    return parents


def better_frontier(list1, list2, type1):

    flag = False

    for x in list1:
        for y in list2:
            if type1(x, y):
                flag = True
                break
        if flag:
            break

    return flag


"Source: https://github.com/ai-se/Spread-HyperVolume/blob/master/HyperVolume/hypervolume_MonteCarlo/HVE.py"


def inbox(pebble, frontier, type1):
    for candidate in frontier:
        if type1(candidate, pebble):
            return True
    return False


def hve(frontier, min, max, type1, sample=100000):
    """estimate hyper volumn of frontier"""
    count = 0
    # print frontier[0]
    m=len(frontier[0].scores)
    for i in xrange(sample):
        pebble=[random.uniform(min[k],max[k]) for k in xrange(m)]
        pebble_can = Candidate(scores=pebble)
        if inbox(pebble_can,frontier,type1):
            count=count+1
    return count/(sample)


# @timing
def ga(model, mp=0.1, cop=1, select=ga_select, population_size=100, num_generations=1000, attempts=5, initial_pop=None):

    # normalize = prerun(model)

    # aggregate = model.aggregate

    # def n_score(indiv):
    #     return normalize(aggregate(indiv))

    # Minimizing
    # If for every objective, indiv1.obj <= indiv2.obj
    # Then indiv1 is better if it's < in at least one
    def type1(indiv1, indiv2):
        # print str(indiv1.scores) + "compared to" + str(indiv2.scores)
        better_flag = False
        for i, score in enumerate(indiv1.scores):
            # if (indiv2.scores[i] < score):
            #     # print "Breaking"
            #     return False

            if (score < indiv2.scores[i]):
                # print "Not there"
                better_flag = True

            elif (score != indiv2.scores[i]):
                return False
            # else:
                # print str(score) + "," + str(indiv2.scores[i])
        # print "Return: " + str(better_flag)
        return better_flag

    obj_mins = [100000000 for _ in range(model.num_objs)]
    obj_maxs = [0 for _ in range(model.num_objs)]

    parents = []

    if initial_pop is None:
        parents = generate_random_population(model, population_size)
    else:
        for can in initial_pop:
            p = Candidate(dec_vals=can.dec_vals, scores=can.scores)
            parents += [p]

    frontier = []

    frontier = generate_frontier(frontier, parents, type1, obj_mins, obj_maxs)

    if len(frontier) == 0:
        frontier = [parents[0], parents[len(parents) - 1]]

    # count = 0

    # while len(frontier) < 1:
    #     frontier = generate_frontier(frontier, parents, type1)
    #     count += 1
    #     print "Attempt:" + str(count)

    lives = 5

    prev_era_frontier = frontier

    for gen_num in range(num_generations):

        children = []

        while len(children) < population_size:

            parent1 = select(parents, type1)
            parent2 = select(parents, type1, exclude=[parent1])

            child1, child2 = crossover(parent1, parent2, cop)
            mutate(child1, mp, model.decs, model.ok)
            mutate(child2, mp, model.decs, model.ok)

            model.eval(child1)
            model.eval(child2)

            if len(children) == population_size - 1:
                if type1(child1, child2):
                    children += [child2]
                else:
                    children += [child1]
            else:
                children += [child1, child2]

        parents = list(children)

        frontier = generate_frontier(frontier, parents, type1, obj_mins, obj_maxs)

        if (gen_num % 100) == 0:
            # print "here"
            if not better_frontier(frontier, prev_era_frontier, type1):
                    # print "WOAH"
                    lives -= 1
                    if lives == 0:
                        # print "Early termination"
                        break
            else:
                lives += 5
            prev_era_frontier = frontier
        # else:
        #     print gen_num
        # print len(frontier)
    # else:
    #     print num_generations

    # if len(frontier) > 50:
    #     print len(frontier)

    # print lives

    # print "Frontier Size:" + str(len(frontier))

    # last_era = [[] for _ in range(model.num_objs)]

    if len(frontier) == 0:
        print "uh oh"
        if attempts == 0:
            return 0
        return ga(model, mp=0.1, cop=1, select=ga_select, population_size=100, num_generations=1000, attempts=attempts - 1)

    return hve(frontier, obj_mins, obj_maxs, type1)

    # for p in frontier:
    #     # print p.dec_vals
    #     # model.eval(p)
    #     for i, score in enumerate(p.scores):
    #         last_era[i] += [score]
    #     # print p.scores
    # # print len(last_era)
    # return last_era
    # for i in range(len(model.decs)):
