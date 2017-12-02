import argparse

def argparser(*add_arguments):
    ret = argparse.ArgumentParser()
    for (args, kwargs) in add_arguments:
        ret.add_argument(*args, **kwargs)
    return ret.parse_args

def argument(*args, **kwargs):
    return args, kwargs
