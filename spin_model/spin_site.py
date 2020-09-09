from numpy.random import randint
from numpy.random import random

class SpinSite(object):
    pass

class IsingSpinSite(SpinSite):
    def __init__(self, config=-1, interaction_strength=1.0, index=1):
        assert isinstance(interaction_strength, float)
        assert isinstance(index,                  int)
        if config in [-1, 1]:
            self.config = config
        else:
            RuntimeError("Wrong config value!")

        self.interaction_strength = interaction_strength
        self.index                = index

    def set_config(self, config):
        if config in [-1, 1]:
            self.config = config
        else:
            RuntimeError("Wrong config value!")

    def set_random_config(self):
        tmp = (-1 if randint(2) else 1)
        self.set_config(tmp)

    def print_site(self):
        pass

    def display_site(self):
        pass
