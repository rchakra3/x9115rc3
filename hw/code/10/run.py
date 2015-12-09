# from model.schaffer import Schaffer
# from model.osyczka2 import Osyczka2
# from model.kursawe import Kursawe
# from model.golinski import Golinski
from model.dtlz import DTLZ1, DTLZ3, DTLZ5, DTLZ7
from model.gamodel import GAModel
from optimizer.ga import ga, generate_random_population
from optimizer.de2 import de
from optimizer.helpers.sk import rdivDemo
import time


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap


@timing
def runner():
    all_eras = []
    for num in range(1):

        for model in [DTLZ5]:  # , Osyczka2, Kursawe, Golinski]:

            era_size = 100

            era0 = []

            objective_numbers = [2]  # , 4, 6, 8]
            decision_numbers = [10]  # , 20, 40]

            for num_objs in objective_numbers:
                for num_decs in decision_numbers:

                    model_id = model.__name__ + "[" + str(num_decs) + "," + str(num_objs)+"]"

                    model_instance = model(num_decs=num_decs, num_objs=num_objs)

                    # era0 = generate_random_population(model_instance, era_size)

                    ga_model_instance = GAModel(3, 1, ga, model_instance)
                    candidates_for_ga = de(ga_model_instance, frontier_size=10, max_tries=1000, threshold=0.1, era_size=10, era0=None, lives=5)

                    best_can = candidates_for_ga[0]

                    for can in candidates_for_ga:
                        if can.scores[0] < best_can.scores[0]:
                            best_can = can

                    mutation_prob_opt = best_can.dec_vals[0]
                    cross_over_points_opt = int(best_can.dec_vals[1])
                    population_size_opt = int(best_can.dec_vals[2])

                    era0 = generate_random_population(model_instance, population_size_opt)

                    modelid = "DTLZ5[10, 2] NO-OP"
                    hv_non_optimized = ga(model_instance, population_size=era_size, num_generations=1000, initial_pop = era0)

                    flag = False
                    for model_hvs in all_eras:
                        if model_hvs[0] == model_id:
                            model_hvs += [hv_non_optimized]
                            flag = True

                    if not flag:
                        curr_model_hv = [model_id, hv_non_optimized]
                        all_eras += [curr_model_hv]

                    # era0_opt = generate_random_population(model_instance, population_size_opt)
                    modelid = "DTLZ5[10, 2] OP"
                    hv_optimized = ga(model_instance, mp=mutation_prob_opt, cop=cross_over_points_opt, population_size=population_size_opt, num_generations=1000, initial_pop=era0)

                    flag = False
                    for model_hvs in all_eras:
                        if model_hvs[0] == model_id:
                            model_hvs += [hv_optimized]
                            flag = True

                    if not flag:
                        curr_model_hv = [model_id, hv_optimized]
                        all_eras += [curr_model_hv]

                    print "NonOptimized HV:" + str(hv_non_optimized)
                    print best_can
                    print "Optimzed HV:" + str(hv_optimized)
                    # for optimizer in [ga]:  # , mws, de]:

                    #     hv = optimizer(model_instance, population_size=era_size, num_generations=1000, initial_pop = era0)
                    #     flag = False
                    #     for model_hvs in all_eras:
                    #         if model_hvs[0] == model_id:
                    #             model_hvs += [hv]
                    #             flag = True

                    #     if not flag:
                    #         curr_model_hv = [model_id, hv]
                    #         all_eras += [curr_model_hv]
                        # print "\n*****************************"
                        # print optimizer.__name__ + "(" + model.__name__ + ")"
                        # era_scores = [model_instance.aggregate(x) for x in last_era]
                        # era_score = [0 for _ in range(len(last_era[0]))]
                        # for can_num in range(len(era_score)):
                        #     for obj_num in range(len(last_era)):
                        #         # print obj_num, can_num
                        #         era_score[can_num] += last_era[obj_num][can_num]
                        #         # if(model.__name__ == "DTLZ7" and num_objs==2 and num_decs==10):
                        #         #     # print last_era[obj_num][can_num]
                        #         #     print len(last_era)

                        # era_score.insert(0, model.__name__ + "[" + str(num_objs) + "," + str(num_decs)+"]")
                        # print era_score
                        # all_eras.append(era_score)
                        # print "*****************************\n"
                # print "Done for obj:" + str(num_objs)
                # print all_eras
    #     print "Iteration " + str(num) + " done!"
    # rdivDemo(all_eras)
    # with open('output_hv.txt', 'w') as f:
    #     for model in all_eras:
    #         for val in model:
    #             f.write(str(val) + ",")
    #         f.write("\n")

runner()
