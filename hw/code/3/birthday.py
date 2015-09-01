from sets import Set
from random import randint


def has_duplicates(list):
    '''Returns true if list has duplicates'''
    unique_vals = Set()
    for val in list:
        if val in unique_vals:
            return True
        unique_vals.add(val)
    return False


def random_num(start, end):
    return randint(start, end)


# Does not take into account leap years
def generate_birthdays_list(size):
    birthdays = []
    for i in range(size):
        birthdays.append(random_num(1, 365))
    return birthdays


def simulate(sample_size):
    ''' Run a single simulation and return True or False'''
    list = generate_birthdays_list(sample_size)
    return has_duplicates(list)


def probability(num_of_sims, sample_size):
    ''' Get the probability of same birthdays
        Takes the sample_size and number of simulations to run as input'''
    true_count = 0

    for i in range(num_of_sims):
        true_count += 1 if simulate(sample_size) else 0

    return (float(true_count) / num_of_sims)


# Run the simulation 10000 times on a sample size of 23
print probability(10000, 23)
