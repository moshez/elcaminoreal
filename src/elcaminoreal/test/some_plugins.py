from elcaminoreal import _gather as gather

_collector = gather.DependencyCollector()

@_collector.register(dependencies=["bar"])
def foo(dependencies, possible_dependencies):
    return dict(bar=dependencies['bar'])

@_collector.register(name="bar")
def bar(dependencies, possible_dependencies):
    return "I'm a bar"

@_collector.register(name="baz")
def baz(dependencies, possible_dependencies):
    return dependencies['bar']

def main(args):
    print(_collector.mkgraph(args))
