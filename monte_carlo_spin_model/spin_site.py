from numpy.random import randint
from numpy.random import uniform
from numpy import pi

class SpinSite(object):
    pass

class IsingSpinSite(SpinSite):
    def __init__(self, config=-1, interaction_strength=1.0, index=1):
        assert isinstance(interaction_strength, float)
        assert isinstance(index,                  int)
        if config in [-1, 1]:
            self._config = config
        else:
            RuntimeError("Wrong config value!")

        self.interaction_strength  = interaction_strength
        self._index                = index

    def get_config(self):
        return self._config

    def get_index(self):
        return self._index

    def set_config(self, config):
        if config in [-1, 1]:
            self._config = config
        else:
            RuntimeError("Wrong config value!")

    def set_random_config(self):
        tmp = (-1 if randint(2) else 1)
        self.set_config(tmp)
        return tmp

    def print_site(self):
        pass

    def display_site(self):
        pass

class XYSpinSite(SpinSite):
    def __init__(self, config=0.0, interaction_strength=1.0, index=1):
        assert isinstance(interaction_strength, float)
        assert isinstance(index,                  int)
        if isinstance(config, float):
            self._config = config
        else:
            RuntimeError("Wrong config value!")

        self.interaction_strength  = interaction_strength
        self._index                = index

    def get_config(self):
        return self._config

    def get_index(self):
        return self._index

    def set_config(self, config):
        if isinstance(config, float):
            self._config = config
        else:
            RuntimeError("Wrong config value!")

    def set_random_config(self):
        random_minus_pi_plus_pi = uniform(-pi, pi)
        self.set_config(random_minus_pi_plus_pi)
        return random_minus_pi_plus_pi

    def print_site(self):
        pass

    def display_site(self):
        pass
