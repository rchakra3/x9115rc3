from random import random


class Osyczka2Solution(object):

    def __init__(self):
        self.ranges = self.generate_ranges()

    def __copy__(self):
        obj = Osyczka2Solution()
        obj.vector = []
        for val in self.vector:
            obj.vector += [val]

        return obj

    def f1(self):
        vec = self.vector
        # print vec
        part1 = 25 * ((vec[0] - 2) ** 2)
        part2 = (vec[1] - 2) ** 2
        part3 = (((vec[2] - 1) ** 2) * ((vec[3] - 4) ** 2))
        part4 = (vec[4] - 1) ** 2

        return (-(part1 + part2 + part3 + part4))

    def f2(self):
        vec = self.vector
        val = 0
        for i in range(0, 6):
            val += vec[i] ** 2

        return val

    def generate_ranges(self):

        ranges = []

        # x1
        ranges += [(0, 10)]
        # x2
        ranges += [(0, 10)]
        # x3
        ranges += [(1, 5)]
        # x4
        ranges += [(0, 6)]
        # x5
        ranges += [(1, 5)]
        # x6
        ranges += [(0, 10)]

        return ranges

    def generate_rand_vec(self):

        vector = []

        while True:
            vector = []
            for i in range(0, 6):
                vector += [self.generate_vec_elem(elem=i, rand=True)]
            if self.validate_vector(vector):
                break

        self.vector = vector

    def random_mutate_element(self, element):

        while True:
            break
            # print "Still here"
            val = self.generate_vec_elem(elem=element, rand=True)  #, debug=True)
            self.vector[element] = val

            if self.validate_vector():
                break
        # print "*********************OUT**********"

    def maximize_score(self, element, score_func):

        steps = 10

        best_x = self.vector[element]
        best_score = score_func(self)

        for i in range(0, steps):

            current_x = self.generate_vec_elem(elem=element, rand=False,
                                               steps=steps, step_num=i)
            self.vector[element] = current_x
            current_score = score_func(self)

            if (current_score > best_score):
                best_score = current_score
                best_x = current_x

        self.vector[element] = best_x

    def validate_vector(self, vector=None):

        if vector is None:
            vector = self.vector

        # print vector

        x1 = vector[0]
        x2 = vector[1]
        x3 = vector[2]
        x4 = vector[3]
        x5 = vector[4]
        x6 = vector[5]

        if not ((x1 + x2) >= 2):
            # print "Failed 1"
            return False

        if not ((x1 + x2) <= 6):
            # print "Failed 2"
            return False

        if not ((x2 - x1) <= 2):
            # print "Failed 3"
            return False

        if not ((x1 - (3 * x2)) <= 2):
            # print "Failed 4"
            return False

        if not ((((x3 - 3) ** 2) + x4) <= 4):
            # print "Failed 5"
            return False

        if not ((((x5 - 3) ** 3) + x6) >= 4):
            # print "Failed 6"
            return False

        return True

    def generate_vec_elem(self, elem=None, rand=None, steps=None, step_num=0, debug=False):

        if elem is None:
            return None

        if rand is None and steps is None:
            # Invalid input
            return None

        min_value, max_value = self.ranges[elem]

        if debug:
            print ("Finding value for x%d between %d and %d" % (elem + 1, min_value, max_value))

        if rand is True:
            return ((random() * (max_value - min_value)) + min_value)

        else:
            if steps is None:
                return None

            if step_num > (steps - 1):
                return None

            step_size = ((max_value - min_value) / steps)

            return (min_value + step_size * step_num)
