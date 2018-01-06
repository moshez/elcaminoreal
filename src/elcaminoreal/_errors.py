import contextlib

import caparg

@contextlib.contextmanager
def errors_to(filep):
    try:
        yield
    except caparg.ParseError as exc:
        filep.write(exc.message)
