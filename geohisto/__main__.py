from datetime import date, datetime

import click

from .loaders import load_counties, load_towns, load_history, load_populations
from .actions import compute
from .exports import write_results_on, generate_head_results_from
from .parents import compute_parents
from .populations import compute_populations
from .specials import compute_specials
from .utils import compute_ancestors


@click.command()
@click.option('--at-date', default=None, multiple=True,
              help='Filter only towns valid at that `YYYY-MM-DD` date.')
def main(at_date):
    # Load data from files.
    towns = load_towns()
    history_list = load_history()
    populations = load_populations()
    counties = load_counties()

    # The order of the different computations is important:
    # ancestors before populations in order to fallback on
    # ancestors' populations sum.
    compute(towns, history_list)
    compute_specials(towns)
    compute_ancestors(towns)
    compute_populations(populations, towns)
    compute_parents(counties, towns)

    # Finally write files.
    write_results_on('exports/towns/towns.csv', towns)
    generate_head_results_from('exports/towns/towns.csv')
    if at_date:
        for date_ in at_date:
            date_ = date(*[int(part) for part in date_.split('-')])
            datetime_ = datetime.combine(date_, datetime.min.time())
            export_path = 'exports/towns/towns_{date_}.csv'.format(
                date_=date_.isoformat())
            write_results_on(export_path, towns, datetime_)


main()
