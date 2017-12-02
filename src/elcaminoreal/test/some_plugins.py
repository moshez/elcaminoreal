import argparse

import elcaminoreal

_commands = elcaminoreal.Commands()

@_commands.dependency(dependencies=["bar"])
def foo(dependencies, possible_dependencies):
    return dict(bar=dependencies['bar'])

@_commands.dependency(name="bar")
def bar(dependencies, possible_dependencies):
    return "I'm a bar"

@_commands.dependency(name="baz")
def baz(dependencies, possible_dependencies):
    return dependencies['bar']

@_commands.dependency(dependencies=['tuck'])
def robin(dependencies, possible_dependencies):
    return dependencies['tuck']

@_commands.dependency(dependencies=['robin'])
def tuck(dependencies, possible_dependencies):
    return dependencies['robin']

parser = argparse.ArgumentParser()
parser.add_argument('lala')
@_commands.command(dependencies=['foo'],
                    parser=parser.parse_args
                    )
def show(args, dependencies):
    print(args, dependencies)

parser = argparse.ArgumentParser()
parser.add_argument('wooo')
@_commands.command(dependencies=['bar'],
                    parser=parser.parse_args)
def gowoo(args, dependencies):
    print("woo", args, dependencies)

def main(args):
    return _commands.run(args[1], args[2:])
