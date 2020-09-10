import numpy

def annealing(spin_sys, temp_init=5.0, temp_final=0.1, nsteps=20,
              max_cycle=1000, tol=1e-4, do_display_config=False):

    dic_thermal = {}
    temp_list = numpy.linspace(temp_init, temp_final, nsteps)
    ene_list  = []
    cv_list   = []

    for temp in temp_list:
        equilibrate(spin_sys, temperature=temp, max_cycle=max_cycle, do_display_config=do_display_config)
        e  = spin_sys.get_energy()
        cv = spin_sys.get_cv()
        ene_list.append(e)
        cv_list.append(cv)

    return temp_list, ene_list


def equilibrate(spin_sys, temperature=None,
                max_cycle=10000, tol=1e-4,
                do_display_config=False):
    if temperature is None:
        temperature = spin_sys.temperature
        beta        = spin_sys.beta
    else:
        if temperature != 0.0:
            spin_sys.set_temperature(temperature)
            beta = 1.0 / temperature
        else:
            RuntimeError("The temperature should not be zero!")

    current_energy = 0.0
    prev_energy    = 0.0
    is_converged   = False
    cycle          = 0
    while (not is_converged) and (cycle < max_cycle):
        self.sweep()
        # list_M.append(np.abs(np.sum(S)/N))
        energy = np.sum(self.get_energy()) / self.num_spins / 2
        dic_thermal_t['energy'] += [energy]
        cycle       += 1
        err          = 1.0 if cycle==0 else abs(current_energy-prev_energy)/abs(current_energy)
        is_converged = err < tol
        
    for k in range(max_cycle):
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
                & (k > 500)) or k == max_cycle - 1:
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
