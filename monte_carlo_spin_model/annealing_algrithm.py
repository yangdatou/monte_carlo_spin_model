import numpy

def annealing(spin_sys, temp_init=5.0, temp_final=0.1, nsteps=20,
              max_cycle=1000, tol=1e-4, do_display_config=False):

    temp_list = numpy.linspace(temp_init, temp_final, nsteps)
    ene_list  = []
    cv_list   = []

    for temp in temp_list:
        e, cv  = equilibrate(spin_sys, temperature=temp, max_cycle=max_cycle, 
                             tol=tol, do_display_config=do_display_config)
        ene_list.append(e)
        cv_list.append(cv)

    return temp_list, ene_list, cv_list


def equilibrate(spin_sys, temperature=None, max_cycle=1000, tol=1e-4,
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

    energy_list    = []
    current_energy = 0.0
    prev_energy    = 0.0
    is_converged   = False
    cycle          = 0
    while (not is_converged) or (cycle < max_cycle//2):
        spin_sys.sweep_system()
        prev_energy    = current_energy
        current_energy = spin_sys.get_system_energy()
        energy_list.append(current_energy)

        if cycle == 0:
            err = 1.0
        else:
            if current_energy == 0.0:
                if prev_energy == 0.0:
                    err = 0.0
                else:
                    err = abs(current_energy-prev_energy)/abs(prev_energy)
            else:
                err = abs(current_energy-prev_energy)/abs(current_energy)
        
        cycle       += 1
        is_converged = err < tol

    if is_converged:
        tmp_array   = numpy.array(energy_list[cycle//2:])
        avg_energy  = numpy.average(tmp_array)
        avg_energy2 = numpy.average(numpy.power(tmp_array,2))
        cv          = (avg_energy2 - avg_energy**2) * beta**2

        print('#T={:6.2f}, sweep={:6d}, energy={:6.2f}, cv={:6.2f}'.format(
            temperature, cycle, avg_energy, cv
            ))
        return avg_energy, cv
    else:
        RuntimeError("MC is not converged!")
    