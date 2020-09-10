from .spin_model import SpinModel

class SpinSystem(object):
    ''' Abstract base class for spin system'''
    pass

class OneDimensionalSpinChain(SpinSystem):
    '''Store the parameters of 1d spin chain'''
    def __init__(self, spin_model, size=10, is_pbc=True, temperature=1.0):
        self.size      = size
        self.is_pbc    = is_pbc
        if temperature != 0.0:
            self.temperature = temperature
            self.beta = 1.0 / temperature
        else:
            RuntimeError("The temperature should not be zero!")

        assert isinstance(spin_model, SpinModel)
        self._spin_model     = spin_model
        self._coord_list     = list(range(size))
        self._spin_site_list = [spin_model.get_site(index=i) for i in range(size)]
        for site in self._spin_site_list:
            site.set_random_config()

        self._spin_site_class  = self._spin_site_list[0].__class__
        self._spin_model_class = self._spin_model.__class__
        self._coord_class      = self._coord_list[0].__class__

    def is_adjacent_coord(self, coord1, coord2):
        assert isinstance(coord1, self._coord_class) 
        assert isinstance(coord2, self._coord_class)
        diff = coord1 - coord2
        assert diff != 0
        if self.is_pbc:
            tmp = (abs(diff) in [1, self.size - 1])
            return tmp
        else:
            tmp = (abs(diff) == 1)
            return tmp

    def is_adjacent_index(self, index1, index2):
        assert isinstance(index1, int) and isinstance(index2, int)
        coord1, coord2 = self._coord_list[index1], self._coord_list[index2]
        tmp = self.is_adjacent_coord(coord1, coord2)
        return tmp

    def is_adjacent_site(self, site1, site2):
        assert isinstance(site1, self._spin_site_class)
        assert isinstance(site2, self._spin_site_class)
        return self.is_adjacent_index(site1.index, site2.index)

    def get_site_neighbors(self, site):
        site_index = site.index

        if self.is_pbc:
            if site_index   == 0:
                return [self._spin_site_list[1], self._spin_site_list[self.size - 1]]
            elif site_index == self.size - 1:
                return [self._spin_site_list[0], self._spin_site_list[self.size - 2]]
        else:
            return [self._spin_site_list[site_index-1], self._spin_site_list[site_index+1]]

    def get_adjacent_pairs(self):
        pair_list = []
        if self.is_pbc:
            for i in range(-1, self.size-1):
                site1 = self._spin_site_list[i]
                site2 = self._spin_site_list[i+1]
                pair_list.append([site1, site2])
        else:
            for i in range(0, self.size-1):
                site1 = self._spin_site_list[i]
                site2 = self._spin_site_list[i+1]
                pair_list.append([site1, site2])
        return pair_list

    def get_int_energy(self, site1, site2):
        factor = (1.0 if self.is_adjacent_site(site1, site2) else 0.0)
        dist   = (1   if self.is_adjacent_site(site1, site2) else 2)
        config1 = site1.config
        config2 = site2.config
        return self._spin_model.get_config_int_energy(config1, config2, dist=dist, factor=factor)

    def get_site_energy(self, site):
        site_neighbors_list = self.get_site_neighbors(site)
        site_energy = 0.0
        for neighbor_site in site_neighbors_list:
            site_energy += self.get_int_energy(site, neighbor_site)

        return site_energy

    def get_system_energy(self):
        adjacent_pairs_list = self.get_adjacent_pairs()

        system_energy = 0.0
        for adjacent_pair in adjacent_pairs_list:
            system_energy += self.get_int_energy(adjacent_pair[0], adjacent_pair[1])

        return system_energy

    def set_spin_site_config(self, index, config):
        self._spin_site_list[index].set_config(config)

    def set_spin_site_random_config(self, index):
        self._spin_site_list[index].set_random_config()

    def set_spin_system_random_config(self):
        for site in self._spin_site_list:
            site.set_random_config()

    def set_temperature(self, temperature):
        if temperature != 0.0:
            self.temperature = temperature
            self.beta = 1.0 / temperature
        else:
            RuntimeError("The temperature should not be zero!")

    def print_system(self):
        pass

    def display_system(self):
        pass
