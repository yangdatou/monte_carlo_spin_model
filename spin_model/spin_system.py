class SpinSystem(object):
    pass

class SpinChain(SpinSystem):
    def __init__(self, spin_model, size = 10, temperature = 1.0, is_pbc = True):
        self._index_list = []
        self._coord_list = []
        self._site_list  = []
