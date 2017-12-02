import functools

import attr

import pyrsistent

import gather

@attr.s(frozen=True)
class DependencyCollector(object):

    _collector = attr.ib(default=attr.Factory(functools.partial(gather.Collector, depth=1)), init=False)

    def register(self,
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
