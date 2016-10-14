import csv
from itertools import islice


def write_results_on(filename, towns):
    """
    Write the `filename` with CSV formatted informations.

    With the generated file, you will be able to retrace the history of
    a given INSEE code with all performed actions as comments.

    Each town has an associated population, sometimes computed from
    population of ancestors.
    """
    with open(filename, 'w') as csvfile:
        fieldnames = [
            'id', 'insee_code', 'name',
            'start_datetime', 'end_datetime',
            'successors', 'ancestors',
            'population', 'insee_modification'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        write = writer.writerow

        for id, town in towns.items():
            write({
                'id': town.id,
                'insee_code': town.depcom,
                'name': town.nccenr,
                'start_datetime': town.start_datetime,
                'end_datetime': town.end_datetime.replace(microsecond=0),
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
