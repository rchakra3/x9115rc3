# from model.schaffer import Schaffer
# from model.osyczka2 import Osyczka2
# from model.kursawe import Kursawe
# from model.golinski import Golinski
from model.dtlz import DTLZ1, DTLZ3, DTLZ5, DTLZ7
from optimizer.ga import ga, generate_random_population
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
    for num in range(20):

        for model in [DTLZ1, DTLZ3, DTLZ5, DTLZ7]:  # , Osyczka2, Kursawe, Golinski]:

            era_size = 100

            era0 = []

            objective_numbers = [2, 4, 6, 8]
            decision_numbers = [10, 20, 40]

            for num_objs in objective_numbers:
                for num_decs in decision_numbers:

                    model_id = model.__name__ + "[" + str(num_decs) + "," + str(num_objs)+"]"

                    model_instance = model(num_decs=num_decs, num_objs=num_objs)

                    era0 = generate_random_population(model_instance, era_size)

                    for optimizer in [ga]:  # , mws, de]:

                        hv = optimizer(model_instance, population_size=era_size, num_generations=1000, initial_pop = era0)
                        flag = False
                        for model_hvs in all_eras:
                            if model_hvs[0] == model_id:
                                model_hvs += [hv]
                                flag = True

                        if not flag:
                            curr_model_hv = [model_id, hv]
                            all_eras += [curr_model_hv]
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
        print "Iteration " + str(num) + " done!"
    rdivDemo(all_eras)
    with open('output_hv.txt', 'w') as f:
        for model in all_eras:
            for val in model:
                f.write(str(val) + ",")
            f.write("\n")

runner()
