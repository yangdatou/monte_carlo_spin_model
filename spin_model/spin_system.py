from .spin_model import SpinModel

class SpinSystem(object):
    pass

class OneDimensionalSpinChain(SpinSystem):
    def __init__(self, spin_model, size=10, is_pbc=True, temperature=1.0):
        self.size = size
        self.is_pbc = is_pbc
        if temperature is not 0.0:
            self.temperature = temperature
            self.beta        = 1.0/temperature
        else:
            RuntimeError("The temperature should not be zero!")

        assert isinstance(spin_model, SpinModel)
        self._spin_model     = spin_model
        self._spin_site_list = [spin_model.get_site(index=i) for i in range(size)]
        self._coord_list     = list(range(size))

        self._spin_site_class  = self._spin_site_list[0].__class__
        self._spin_model_class = self._spin_model.__class__
        self._coord_class      = self._coord_list[0].__class__


    def is_adjacent_coord(self, coord1, coord2):
        assert isinstance(coord1, self._coord_class) and isinstance(coord2, self._coord_class)

        diff = coord1 - coord2
        assert  diff is not 0
        if self.is_pbc:
            tmp = (abs(diff) in [1, self.size-1])
            return tmp
        else:
            tmp = (abs(diff) is 1)
            return tmp

    def is_adjacent_index(self, index1, index2):
        assert isinstance(index1, int) and isinstance(index2, int)
        return self.is_adjacent_coord(self._coord_list[index1], self._coord_list[index2])

    def is_adjacent_site(self, site1, site2):
        assert isinstance(site1, self._spin_site_class) and isinstance(site2, self._spin_site_class)
        return self.is_adjacent_index(site1.index, site1.index)

    def get_site_neighbors(self, site):
        site_index = site.index
        if self.is_pbc:
            if site_index is 0:
                return [1, self.size-1]
            elif site_index is self.size-1:
                return 
        else:
            tmp = (abs(diff) is 1)
            return tmp