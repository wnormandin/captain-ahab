import random


def random_wait():
    return random.random() * 0.5


def random_float(minimum=0.0, maximum=1.0):
    return random.uniform(minimum, maximum)

