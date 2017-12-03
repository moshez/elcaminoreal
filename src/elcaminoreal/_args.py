"""
An experiment in a better way to build argument parsers.
"""
import argparse

import attr


def argparser(*things):
    """
    Generate a function that parses arguments.
    """
    ret = argparse.ArgumentParser()
    for thing in things:
        thing.add_to(ret)
    return ret.parse_args


@attr.s(frozen=True)
class argument(object):

    name = attr.ib()
    required = attr.ib(default=False)

    def add_to(self, parser):
        kwargs = {}
        if self.required:
            kwargs['required'] = True
        parser.add_argument(self.name, **kwargs)
