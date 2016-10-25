from datetime import date, datetime

import click

from .loaders import load_towns, load_history, load_populations
from .actions import compute
from .utils import compute_ancestors
from .populations import compute_populations
from .exports import write_results_on, generate_head_results_from


@click.command()
@click.option('--at-date', default=None,
              help='Filter only towns valid at that `YYYY-MM-DD` date.')
def main(at_date):
    if at_date:
        at_date = date(*[int(part) for part in at_date.split('-')])
        at_datetime = datetime.combine(at_date, datetime.min.time())

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
    if at_date:
        export_path = 'exports/towns/towns_{at_date}.csv'.format(
            at_date=at_date.isoformat())
        write_results_on(export_path, towns, at_datetime)
    else:
        write_results_on('exports/towns/towns.csv', towns)
        generate_head_results_from('exports/towns/towns.csv')


main()
