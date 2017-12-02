from elcaminoreal import _gather as gather

_collector = gather.DependencyCollector()

@_collector.dependency(dependencies=["bar"])
def foo(dependencies, possible_dependencies):
    return dict(bar=dependencies['bar'])

@_collector.dependency(name="bar")
def bar(dependencies, possible_dependencies):
    return "I'm a bar"

@_collector.dependency(name="baz")
def baz(dependencies, possible_dependencies):
    return dependencies['bar']

@_collector.dependency(dependencies=['tuck'])
def robin(dependencies, possible_dependencies):
    return dependencies['tuck']

@_collector.dependency(dependencies=['robin'])
def tuck(dependencies, possible_dependencies):
    return dependencies['robin']

@_collector.command(dependencies=['foo'])
def show(args, dependencies):
    print(args, dependencies)

@_collector.command(dependencies=['bar'])
def gowoo(args, dependencies):
    print("woo", args, dependencies)

def main(args):
    return _collector.run(args[1], args[2:])
