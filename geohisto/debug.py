"""Useful snippets to debug actions."""
from pprint import pprint


def debug_by_depcom(*depcoms):
    """Decorator to be applied on actions to debug a particular case."""
    def wrap(f):
        def wrapped_f(towns, record):
            print(f.__name__, 'will happen')
            print(record)
            for depcom in depcoms:
                pprint(towns.filter(depcom=depcom))
            f(towns, record)
            print(f.__name__, 'happened')
            for depcom in depcoms:
                pprint(towns.filter(depcom=depcom))
            print('*' * 90)
        return wrapped_f
    return wrap
