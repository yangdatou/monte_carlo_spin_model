from numpy import exp
from numpy import random

from .spin_model import SpinModel

class SpinSystem(object):
    ''' Abstract base class for spin system'''
    def is_adjacent_coord(self, coord1, coord2):
        pass

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
        tmp    = self.is_adjacent_index(index1, index2)
        return tmp

    def get_index(self, site):
        assert isinstance(site, self._spin_site_class)
        site_index = site.get_index()
        return site_index

    def get_site(self, index):
        sys_size = self.size
        assert isinstance(index, int)
        assert 0 <= index and index < sys_size
        site = self._spin_site_list[index]
        return site

    def get_index_config(self, index):
        return self._spin_site_list[index].get_config()

    def get_site_config(self, site):
        return site.get_config()

    def get_coord_neighbors(self, coord):
        pass

    def get_index_neighbors(self, index):
        assert isinstance(index, int)
        coord = self._coord_list[index]
        coord_neighbor_list  = self.get_coord_neighbors(coord)
        index_neighbor_list  = []
        for tmp_coord in coord_neighbor_list:
            tmp_idx = self._coord_list.index(tmp_coord)
            index_neighbor_list.append(tmp_idx)
        return index_neighbor_list

    def get_site_neighbors(self, site):
        assert isinstance(site, self._spin_site_class)
        index = site.get_index()
        coord = self._coord_list[index]
        coord_neighbor_list  = self.get_coord_neighbors(coord)
        site_neighbor_list   = []
        for tmp_coord in coord_neighbor_list:
            tmp_idx  = self._coord_list.index(tmp_coord)
            tmp_site = self.get_site(tmp_idx)
            site_neighbor_list.append(tmp_site)
        return site_neighbor_list

    def get_adjacent_coord_pairs(self):
        pass

    def get_adjacent_index_pairs(self):
        coord_pair_list = self.get_adjacent_coord_pairs()
        index_pair_list = []
        for coord_pair in coord_pair_list:
            coord1 = coord_pair[0]
            coord2 = coord_pair[1]
            tmp_pair = (self._coord_list.index(coord1), self._coord_list.index(coord2))
            index_pair_list.append(tmp_pair)
        return index_pair_list

    def get_adjacent_site_pairs(self):
        coord_pair_list = self.get_adjacent_coord_pairs()
        site_pair_list  = []
        for coord_pair in coord_pair_list:
            coord1 = coord_pair[0]
            coord2 = coord_pair[1]
            index1 = self._coord_list.index(coord1)
            index2 = self._coord_list.index(coord2)
            site1  = self.get_site(index1)
            site2  = self.get_site(index2)
            tmp_pair = (site1, site2)
            site_pair_list.append(tmp_pair)
        return site_pair_list

    def get_site_int_energy(self, site1, site2):
        assert isinstance(site1, self._spin_site_class)
        assert isinstance(site2, self._spin_site_class)

        factor  = (1.0 if self.is_adjacent_site(site1, site2) else 0.0)
        dist    = (1   if self.is_adjacent_site(site1, site2) else 2)
        config1 = site1.get_config()
        config2 = site2.get_config()
        return self._spin_model.get_config_int_energy(config1, config2, dist=dist, factor=factor)

    def get_site_energy(self, site):
        site_neighbors_list = self.get_site_neighbors(site)
        site_energy = 0.0

        if self.z_field is not None:
            field        = self.z_field
            config       = site.get_config()
            site_energy += self._spin_model.get_field_energy(config, field)

        for neighbor_site in site_neighbors_list:
            site_energy += self.get_site_int_energy(site, neighbor_site)

        return site_energy

    def get_system_energy(self):
        system_energy = 0.0
        if self.z_field is not None:
            field        = self.z_field
            for site in self._spin_site_list:
                config       = site.get_config()
                site_energy += self._spin_model.get_field_energy(config, field)
        adjacent_pairs_list = self.get_adjacent_site_pairs()
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

class OneDimensionalSpinChain(SpinSystem):
    '''Store the parameters of 1d spin chain'''
    def __init__(self, spin_model, shape=10, is_pbc=True, z_field=None,temperature=1.0):
        self.shape     = shape
        self.size      = shape
        self.is_pbc    = is_pbc
        self.z_field   = z_field
        if temperature != 0.0:
            self.temperature = temperature
            self.beta = 1.0 / temperature
        else:
            RuntimeError("The temperature should not be zero!")

        assert isinstance(spin_model, SpinModel)
        self._spin_model     = spin_model
        self._coord_list     = list(range(shape))
        self._spin_site_list = [spin_model.make_site(index=i) for i in range(self.size)]
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
            tmp = (abs(diff) in [1, self.shape - 1])
            return tmp
        else:
            tmp = (abs(diff) == 1)
            return tmp

    def get_coord_neighbors(self, coord):
        assert isinstance(coord, self._coord_class) 
        sys_size  = self.size
        sys_shape = self.shape
        if self.is_pbc:
            if   coord == 0:
                return [sys_shape - 1, 1]
            elif coord == sys_shape - 1:
                return [sys_shape - 2, 0]
            else:
                return [coord - 1, coord + 1]
        else:
            if coord   == 0:
                return [1]
            elif coord == sys_shape - 1:
                return [sys_shape - 2]
            else:
                return [coord - 1, coord + 1]

    def get_adjacent_coord_pairs(self):
        sys_size  = self.size
        sys_shape = self.shape
        if self.is_pbc:
            tmp_pair_list = [(sys_shape-1, 0)]
        else:
            tmp_pair_list = []

        for i in range(0, sys_size-1):
            tmp_pair_list.append((i, i+1))

        if self.is_pbc:
            assert len(tmp_pair_list) == sys_size
        else:
            assert len(tmp_pair_list) == sys_size - 1
        return tmp_pair_list

class TwoDimensionalSpinLattice(SpinSystem):
    def __init__(self, spin_model, shape=10, is_pbc=True, z_field=None, temperature=1.0):
        self.shape     = shape
        self.size      = shape*shape
        self.is_pbc    = is_pbc
        self.z_field   = z_field
        if temperature != 0.0:
            self.temperature = temperature
            self.beta = 1.0 / temperature
        else:
            RuntimeError("The temperature should not be zero!")

        assert isinstance(spin_model, SpinModel)
        self._spin_model     = spin_model
        self._coord_list     = [(i,j) for i in range(shape) for j in range(shape)]
        self._spin_site_list = [spin_model.make_site(index=i) for i in range(self.size)]
        for site in self._spin_site_list:
            site.set_random_config()

        self._spin_site_class  = self._spin_site_list[0].__class__
        self._spin_model_class = self._spin_model.__class__
        self._coord_class      = self._coord_list[0].__class__

    def is_adjacent_coord(self, coord1, coord2):
        assert isinstance(coord1, self._coord_class) 
        assert isinstance(coord2, self._coord_class)
        sys_size  = self.size
        sys_shape = self.shape
        diff_x    = coord1[0] - coord2[0]
        diff_y    = coord1[1] - coord2[1]
        assert diff_x != 0 or diff_y != 0

        if self.is_pbc:
            tmp = (abs(diff_x) in [1, sys_shape - 1]) and (abs(diff_y) in [1, sys_shape - 1])
            return tmp
        else:
            tmp = (abs(diff_x) == 1) and (abs(diff_y) == 1)
            return tmp

    def get_adjacent_coord_pairs(self):
        sys_size   = self.size
        sys_shape  = self.shape

        tmp_pair_list = []
        if self.is_pbc:
            for i in range(sys_shape):
                tmp_pair_list.append(((0,i), (sys_shape-1,i)))
                tmp_pair_list.append(((i,i), (i,sys_shape-1)))
        for i in range(sys_shape-1):
            for j in range(sys_shape-1):
                tmp_pair_list.append(((i,j), (i+1,j)))
                tmp_pair_list.append(((i,j), (i,j+1)))
        for i in range(sys_shape-1):
            tmp_pair_list.append(((sys_shape-1,i), (sys_shape-1,i+1)))
            tmp_pair_list.append(((i,sys_shape-1), (i+1,sys_shape-1)))
        if self.is_pbc:
            assert len(tmp_pair_list) == 2*sys_size
        else:
            assert len(tmp_pair_list) == 2*sys_size - 2*sys_shape
        return tmp_pair_list
