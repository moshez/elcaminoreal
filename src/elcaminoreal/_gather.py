import argparse
import functools

import attr

import pyrsistent

import gather

@attr.s(frozen=True)
class Commands(object):

    """
    Collect commands and stuff
    """

    _collector = attr.ib(default=attr.Factory(functools.partial(gather.Collector, depth=1)), init=False)
    _command_collector = attr.ib(default=attr.Factory(functools.partial(gather.Collector, depth=1)), init=False)

    def command(self,
                name=None,
                parser=argparse.ArgumentParser(),
                dependencies=pyrsistent.v()):
        transform = gather.Wrapper.glue((dependencies, parser))
        ret = self._command_collector.register(name, transform=transform)
        return ret

    def run(self, args, override_dependencies=pyrsistent.m()):
        name, args = args[0], args[1:]
        collection = self._command_collector.collect() 
        command = collection[name]
        func = command.original
        dependencies, parser = command.extra
        graph = self.mkgraph(dependencies)
        graph.update(override_dependencies)
        parsed = parser(args)
        return func(parsed, graph)

    def dependency(self,
                   name=None,
                   dependencies=pyrsistent.v(),
                   possible_dependencies=pyrsistent.v()):
        glue = (dependencies, possible_dependencies)
        transform = transform=gather.Wrapper.glue(glue)
        ret = self._collector.register(name, transform=transform)
        return ret

    # Recursive implementation for now
    def mkgraph(self, things):
        collection = self._collector.collect()
        ret = {}
        def build(thing, on_route=pyrsistent.s()):
            if thing in on_route:
                raise ValueError("circular dependency detected",
                                 thing, on_route)
            if thing in ret:
                return ret[thing]
            on_route = on_route.add(thing)
            plugin = collection[thing]
            func = plugin.original
            dependencies, possible_dependencies = plugin.extra
            my_dependencies, my_possible_dependencies = {}, {}
            for other_thing in dependencies:
                my_dependencies[other_thing] = build(other_thing, on_route)
            for other_thing in possible_dependencies:
                builder = functools.partial(build, other_thing, on_route)
                my_possible_dependencies[other_thing] = builder
            ret[thing] = func(my_dependencies, my_possible_dependencies)
            return ret[thing]
        for thing in things:
            build(thing)
        return ret
