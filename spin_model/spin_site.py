from numpy.random import randint
from numpy.random import random

class SpinSite(object):
    pass

class IsingSpinSite(SpinSite):
    def __init__(self, config = 0, interaction_strength = 1.0, index = 1):
        self.interaction_strength = interaction_strength
        self.index = index

        if config in [-1,1]:
            self.config = config
        else:
            RuntimeError("Wrong config value!")

    def set_config(self, config):
        if config in [0,1]:
            self.config = config

    def set_random_config(self):
        temp = randint(2)
        self.set_config(temp)

    def get_int_energy(self, other_site):
        pass

    def do_something(self):
        pass