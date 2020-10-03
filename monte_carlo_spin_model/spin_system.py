from numpy import exp
from numpy import random

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
        self._spin_site_list = [spin_model.make_site(index=i) for i in range(size)]
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

        index1 = site1.get_index()
        index2 = site2.get_index()

        return self.is_adjacent_index(index1, index2)

    def get_site(self, index):
        sys_size = self.size
        assert isinstance(index, int)
        assert 0 <= index and index < sys_size

        site = self._spin_site_list[index]
        return site

    def get_index(self, site):
        assert isinstance(site, self._spin_site_class)
        site_index = site.get_index()
        return site_index

    def get_site_config(self, site):
        return site.get_config()

    def get_index_config(self, index):
        return self._spin_site_list[index].get_config()

    def get_index_neighbors(self, index):
        assert isinstance(index, int)
        sys_size = self.size

        if self.is_pbc:
            if index   == 0:
                return [sys_size - 1, 1]
            elif index == self.size - 1:
                return [sys_size - 2, 0]
            else:
                return [index - 1, index + 1]
        else:
            if index   == 0:
                return [1]
            elif index == self.size - 1:
                return [sys_size - 2]
            else:
                return [index - 1, index + 1]

    def get_site_neighbors(self, site):
        assert isinstance(site, self._spin_site_class)

        spin_index           = site.get_index()
        index_neighbors_list = self.get_index_neighbors(spin_index)
        site_neighbors_list  = [self.get_site(i) for i in index_neighbors_list]
        return site_neighbors_list

    def get_adjacent_index_pairs(self):
        sys_size  = self.size
    
        if self.is_pbc:
            pair_list = [(sys_size-1, 0)]
        else:
            pair_list = []

        for i in range(0, sys_size-1):
            pair_list.append((i, i+1))
        return pair_list

    def get_adjacent_site_pairs(self):
        sys_size  = self.size
    
        if self.is_pbc:
            site1 = self.get_site(sys_size-1)
            site2 = self.get_site(0)
            pair_list = [(site1, site2)]
        else:
            pair_list = []

        for i in range(0, sys_size-1):
            site1 = self.get_site(i)
            site2 = self.get_site(i+1)
            pair_list.append((site1, site2))
        return pair_list

    def get_site_int_energy(self, site1, site2):
        assert isinstance(site1, self._spin_site_class)
        assert isinstance(site2, self._spin_site_class)

        factor = (1.0 if self.is_adjacent_site(site1, site2) else 0.0)
        dist   = (1   if self.is_adjacent_site(site1, site2) else 2)
        config1 = site1.get_config()
        config2 = site2.get_config()
        return self._spin_model.get_config_int_energy(config1, config2, dist=dist, factor=factor)

    def get_site_energy(self, site):
        site_neighbors_list = self.get_site_neighbors(site)
        site_energy = 0.0

        for neighbor_site in site_neighbors_list:
            site_energy += self.get_site_int_energy(site, neighbor_site)

        return site_energy

    def get_system_energy(self):
        adjacent_pairs_list = self.get_adjacent_site_pairs()
        system_energy = 0.0

        for adjacent_pair in adjacent_pairs_list:
            system_energy += self.get_site_int_energy(adjacent_pair[0], adjacent_pair[1])

        return system_energy

    def set_temperature(self, temperature):
        if temperature != 0.0:
            self.temperature = temperature
            self.beta = 1.0 / temperature
        else:
            RuntimeError("The temperature should not be zero!")

    def set_index_config(self, index, config):
        assert isinstance(index, int)
        site = self.get_site(index)
        site.set_config(config)

    def set_site_config(self, site, config):
        assert isinstance(site, self._spin_site_class)
        site.set_config(config)

    def sweep_site(self, site):
        assert isinstance(site, self._spin_site_class)

        prev_config    = self.get_site_config(site)
        prev_energy    = self.get_site_energy(site)
        current_config = site.set_random_config()
        current_energy = self.get_site_energy(site)

        diff_energy    = current_energy - prev_energy
        exp_beta_e     = exp(-self.beta*diff_energy)
        random_0_1     = random.random()

        do_accept      = (random_0_1 < exp_beta_e)

        if not do_accept:
            self.set_site_config(site, prev_config)

    def sweep_system(self):
        for isite, site in enumerate(self._spin_site_list):
            self.sweep_site(site)

    def print_system(self):
        pass

    def display_system(self):
        pass

class TwoDimensionalSpinLattice(SpinSystem):
    pass