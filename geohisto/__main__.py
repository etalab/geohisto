from datetime import date, datetime

import click
import click_log

from .actions import compute
from .exports import generate_head_results_from, write_results_on
from .intercommunalities import load_intercommunalities
from .intercommunalities import write_intercommunalities_on
from .loaders import load_counties, load_history, load_populations, load_towns
from .parents import compute_parents
from .populations import compute_populations
from .specials import compute_specials
from .utils import compute_ancestors


@click.command()
@click.option('--at-date', default=None, multiple=True,
              help='Filter only towns valid at that `YYYY-MM-DD` date.')
@click.option('-i', '--intercommunalities', is_flag=True,
              help='Process intercommunalities')
@click_log.simple_verbosity_option()
@click_log.init('geohisto')
def main(at_date, intercommunalities):
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
    if intercommunalities:
        intercommunalities = load_intercommunalities(towns)

    # Finally write files.
    write_results_on('exports/communes/communes.csv', towns)
    generate_head_results_from('exports/communes/communes.csv')
    if intercommunalities:
        write_intercommunalities_on('exports/epci/epci.csv',
                                    intercommunalities)
        generate_head_results_from('exports/epci/epci.csv')
    if at_date:
        for date_ in at_date:
            date_ = date(*[int(part) for part in date_.split('-')])
            datetime_ = datetime.combine(date_, datetime.min.time())
            export_path = 'exports/communes/communes_{date_}.csv'.format(
                date_=date_.isoformat())
            write_results_on(export_path, towns, datetime_)
            if intercommunalities:
                export_path = 'exports/epci/epci_{date_}.csv'.format(
                    date_=date_.isoformat())
                write_intercommunalities_on(export_path,
                                            intercommunalities,
                                            date_)


main()
