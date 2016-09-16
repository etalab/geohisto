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
            'ID', 'INSEE_CODE', 'NAME',
            'START_DATETIME', 'END_DATETIME',
            'SUCCESSORS', 'ANCESTORS',
            'POPULATION', 'COMMENT'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        write = writer.writerow

        for id, town in towns:
            # Main entry.
            write({
                'ID': town.id,
                'INSEE_CODE': town.depcom,
                'NAME': town.nccenr,
                'START_DATETIME': town.start_datetime,
                'END_DATETIME': town.end_datetime,
                'SUCCESSORS': town.successors,
                'ANCESTORS': town.ancestors,
                'POPULATION': town.population,
                'COMMENT': town.modification
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
