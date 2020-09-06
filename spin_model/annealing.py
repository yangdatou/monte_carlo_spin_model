def annealing(T_init=2.5, T_final=0.1, nsteps=20, show_equi=False):
    # initialize spins. Orientations are taken from 0 - 2pi randomly.
    # initialize spin configuration
    dic_thermal = {}
    dic_thermal['temperature'] = list(np.linspace(T_init, T_final, nsteps))
    dic_thermal['energy'] = []
    dic_thermal['Cv'] = []
    for T in dic_thermal['temperature']:
        self.equilibrate(temperature=T)
        if show_equi:
            self.show()
        dic_thermal['energy'] += [self.energy]
        dic_thermal['Cv'] += [self.Cv]
    plt.plot(dic_thermal['temperature'], dic_thermal['Cv'], '.')
    plt.ylabel(r'$C_v$')
    plt.xlabel('T')
    plt.show()
    plt.plot(dic_thermal['temperature'], dic_thermal['energy'], '.')
    plt.ylabel(r'$\langle E \rangle$')
    plt.xlabel('T')
    plt.show()
    return dic_thermal


def equilibrate(
        self,
        max_nsweeps=int(1e4),
        temperature=None,
        H=None,
        show=False):
    if temperature is not None:
        self.temperature = temperature
    dic_thermal_t = {}
    dic_thermal_t['energy'] = []
    beta = 1.0 / self.temperature
    energy_temp = 0
    for k in list(range(max_nsweeps)):
        self.sweep()
        # list_M.append(np.abs(np.sum(S)/N))
        energy = np.sum(self.get_energy()) / self.num_spins / 2
        dic_thermal_t['energy'] += [energy]
        #print( abs(energy-energy_temp)/abs(energy))
        if show & (k % 1e3 == 0):
            print('#sweeps=%i' % (k + 1))
            print('energy=%.2f' % energy)
            self.show()
        if ((abs(energy - energy_temp) / abs(energy) < 1e-4)
                & (k > 500)) or k == max_nsweeps - 1:
            print(
                '\nequilibrium state is reached at T=%.1f' %
                self.temperature)
            print('#sweep=%i' % k)
            print('energy=%.2f' % energy)
            break
        energy_temp = energy
    nstates = len(dic_thermal_t['energy'])
    energy = np.average(dic_thermal_t['energy'][int(nstates / 2):])
    self.energy = energy
    energy2 = np.average(
        np.power(dic_thermal_t['energy'][int(nstates / 2):], 2))
    self.Cv = (energy2 - energy**2) * beta**2
