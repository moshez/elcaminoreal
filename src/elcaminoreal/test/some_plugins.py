import argparse
import random

import elcaminoreal

COMMANDS = elcaminoreal.Commands()

@COMMANDS.dependency(dependencies=["bar"])
def foo(dependencies, possible_dependencies):
    return dict(bar=dependencies['bar'])

@COMMANDS.dependency(possible_dependencies=["bar"])
def foo_2(dependencies, possible_dependencies):
    return dict(bar=possible_dependencies['bar']())

@COMMANDS.dependency()
def bar(dependencies, possible_dependencies):
    return "I'm a bar"

@COMMANDS.dependency()
def rand(dependencies, possible_dependencies):
    return random.random()

@COMMANDS.dependency(dependencies=["rand"])
def needs_rand(dependencies, possible_dependencies):
    return dict(rand=dependencies["rand"])

@COMMANDS.dependency(name="baz")
def baz(dependencies, possible_dependencies):
    return dependencies['bar']

@COMMANDS.dependency(dependencies=['tuck'])
def robin(dependencies, possible_dependencies):
    return dependencies['tuck']

@COMMANDS.dependency(dependencies=['robin'])
def tuck(dependencies, possible_dependencies):
    return dependencies['robin']

@COMMANDS.command(dependencies=['foo'],
                  parser=elcaminoreal.argparser(
                      elcaminoreal.argument('lala'),
                  ))
def show(args, dependencies):
    print(args, dependencies)

@COMMANDS.command(dependencies=['bar'],
                  parser=elcaminoreal.argparser(
                      elcaminoreal.argument('wooo'),
                  ))
def gowoo(args, dependencies):
    print("woo", args, dependencies)
