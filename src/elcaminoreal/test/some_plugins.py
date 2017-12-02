import argparse

import elcaminoreal

COMMANDS = elcaminoreal.Commands()

@COMMANDS.dependency(dependencies=["bar"])
def foo(dependencies, possible_dependencies):
    return dict(bar=dependencies['bar'])

@COMMANDS.dependency(name="bar")
def bar(dependencies, possible_dependencies):
    return "I'm a bar"

@COMMANDS.dependency(name="baz")
def baz(dependencies, possible_dependencies):
    return dependencies['bar']

@COMMANDS.dependency(dependencies=['tuck'])
def robin(dependencies, possible_dependencies):
    return dependencies['tuck']

@COMMANDS.dependency(dependencies=['robin'])
def tuck(dependencies, possible_dependencies):
    return dependencies['robin']

parser = argparse.ArgumentParser()
parser.add_argument('lala')
@COMMANDS.command(dependencies=['foo'],
                    parser=parser.parse_args
                    )
def show(args, dependencies):
    print(args, dependencies)

parser = argparse.ArgumentParser()
parser.add_argument('wooo')
@COMMANDS.command(dependencies=['bar'],
                    parser=parser.parse_args)
def gowoo(args, dependencies):
    print("woo", args, dependencies)
