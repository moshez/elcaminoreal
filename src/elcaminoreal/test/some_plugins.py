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
