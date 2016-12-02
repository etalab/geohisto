import csv
from itertools import islice


def write_results_on(filename, towns, at_datetime=None):
    """
    Write the `filename` with CSV formatted informations.

    With the generated file, you will be able to retrace the history of
    a given INSEE code with all performed actions as comments.

    Each town has an associated population, sometimes computed from
    population of ancestors.

    The `at_datetime` parameter allows you to only filter valid towns at
    that given datetime.
    """
    with open(filename, 'w') as csvfile:
        fieldnames = [
            'id', 'insee_code',
            'start_datetime', 'end_datetime',
            'name',
            'successors', 'ancestors',
            'population', 'insee_modification'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        write = writer.writerow

        if at_datetime:
            towns = towns.valid_at(at_datetime)
        else:
            towns = towns.values()

        for town in towns:
            write({
                'id': town.id,
                'insee_code': town.depcom,
                'start_datetime': town.start_datetime,
                'end_datetime': town.end_datetime.replace(microsecond=0),
                'name': town.nccenr,
                'successors': town.successors,
                'ancestors': town.ancestors,
                'population': town.population,
                'insee_modification': town.modification
            })


def generate_head_results_from(filename, nb_of_lines=100):
    """
    Equivalent of `head` using Python.

    The passed `filename` will have a `_head` suffix added for the
    newly generated extract.
    """
    filepath, extension = filename.split('.')
    filename_out = filepath + '_head.' + extension
    with open(filename) as csvfile, \
            open(filename_out, 'w') as csvfileout:
        head = islice(csvfile, nb_of_lines)
        csvfileout.write(''.join(head))
