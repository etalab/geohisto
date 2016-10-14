from .loaders import load_towns, load_history, load_populations
from .actions import compute
from .utils import compute_ancestors
from .populations import compute_populations
from .exports import write_results_on, generate_head_results_from

# Load data from files.
towns = load_towns()
history_list = load_history()
populations = load_populations()

# The order of the different computations is important:
# ancestors before populations in order to fallback on
# ancestors' populations sum.
compute(towns, history_list)
compute_ancestors(towns)
compute_populations(populations, towns)

# Finally write files.
write_results_on('exports/towns/towns.csv', towns)
generate_head_results_from('exports/towns/towns.csv')
