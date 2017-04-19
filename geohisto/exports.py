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
            'successors', 'ancestors', 'parents',
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
                'parents': town.parents,
                'population': town.population,
                'insee_modification': town.modification
            })


def generate_head_results_from(filename_in, nb_of_lines=100):
    """
    Equivalent of `head` shell command using Python.

    The passed `filename_in` will have a `_head` suffix added for the
    newly generated extract.
    """
    filepath, extension = filename_in.split('.')
    filename_out = filepath + '_head.' + extension
    with open(filename_in) as file_in, open(filename_out, 'w') as file_out:
        head = islice(file_in, nb_of_lines)
        file_out.write(''.join(head))
