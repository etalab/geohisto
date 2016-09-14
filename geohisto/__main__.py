from .loaders import load_towns, load_history, load_populations
from .actions import do_all_actions
from .utils import compute_ancestors
from .populations import compute_populations
from .exports import write_results_on, generate_head_results_from


towns = load_towns()
history_list = load_history()
towns, history_list = do_all_actions(towns, history_list)
towns = compute_ancestors(towns)
populations = load_populations()
towns = compute_populations(populations, towns)
write_results_on('exports/towns/towns.csv', towns)
generate_head_results_from('exports/towns/towns.csv')
