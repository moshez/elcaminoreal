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

t = []

def main(args):
    t.append(1)
    print(_collector.mkgraph(args))
    if len(t) > 1:
        raise ValueError(args)
