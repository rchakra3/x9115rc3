import random


class Decision(object):

    def __init__(self, name, min_val, max_val, type="range"):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.type = type

    def generate_valid_val(self):
        if self.type == "int":
            return random.randint(self.min_val, self.max_val)
        return random.uniform(self.min_val, self.max_val)

    def get_range(self):
        return (self.min_val, self.max_val)

    def wrap(self, value):
        return self.min_val + (value - self.min_val) % (self.max_val - self.min_val)
