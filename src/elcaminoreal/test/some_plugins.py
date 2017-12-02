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

@_collector.register(dependencies=['tuck'])
def robin(dependencies, possible_dependencies):
    return dependencies['tuck']

@_collector.register(dependencies=['robin'])
def tuck(dependencies, possible_dependencies):
    return dependencies['robin']

def main(args):
    print(_collector.mkgraph(args))
