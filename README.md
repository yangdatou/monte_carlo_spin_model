# Monte Carlo Spin Model
A `Python` implementation of the basic Monte Carlo to algorithm in differebt spin models.

## Spin Models `SpinModel` and `SpinSite`
- Ising model `IsingModel` and `IsingSpinSite`
- XY model

## Spin System `SpinSystem`
- 1D spin chain `OneDimensionalSpinChain`
- 2D square lattice

## Example

```
import monte_carlo_spin_model
from   monte_carlo_spin_model.spin_system         import OneDimensionalSpinChain
from   monte_carlo_spin_model.spin_model          import IsingModel
from   monte_carlo_spin_model.annealing_algrithm  import equilibrate, annealing

coulping_const = 1.0
nn             = 20

ising_model = IsingModel(interaction_strength=coulping_const)
spin_chain  = OneDimensionalSpinChain(ising_model, size=nn, is_pbc=True)

equilibrate(spin_chain, temperature=10.0, max_cycle=2000, tol=1e-4)
temp_list, ene_list, cv_list = annealing(
    spin_chain, temp_init=5.0, temp_final=0.1, nsteps=20, max_cycle=2000, tol=1e-4
)
```
