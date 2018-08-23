"""
Gather dependencies and commands
"""
import functools

import attr
import caparg
import gather
import pyrsistent

_COLLECTOR_FACTORY = attr.Factory(functools.partial(gather.Collector, depth=1))


@attr.s(frozen=True)
class ExtraData(object):
    """
    Metadata about commands
    """
    parser = attr.ib(default=caparg.command(''))
    dependencies = attr.ib(default=pyrsistent.v())
    aliases = attr.ib(default=pyrsistent.v())
    regular = attr.ib(default=False)


@attr.s(frozen=True)
class Commands(object):

    """
    A command and dependency gatherer.
    """

    _collector = attr.ib(default=_COLLECTOR_FACTORY, init=False)
    _command_collector = attr.ib(default=_COLLECTOR_FACTORY, init=False)

    def command(self,
                name=None,
                **kwargs):
        """
        Register as a command.

        """
        transform = gather.Wrapper.glue(ExtraData(**kwargs))
        ret = self._command_collector.register(name, transform=transform)
        return ret

    def get_commands(self):
        """
        Get all commands
        """
        collection = {name.replace('_', '-'): value
                      for name, value in
                      self._command_collector.collect().items()}
        for thing in list(collection.values()):
            for alias in thing.extra.aliases:
                collection[alias] = thing
        return collection

    def run(self, args, override_dependencies=pyrsistent.m()):
        """
        Run a command

        """
        collection = self.get_commands()
        subcommands = [thing.extra.parser.rename(name)
                       for name, thing in collection.items()]
        command = caparg.command('', *subcommands)
        parsed = command.parse(args)
        subcommand = ' '.join(parsed['__caparg_subcommand__'])
        func = collection[subcommand].original
        extra = collection[subcommand].extra
        graph = self.mkgraph(extra.dependencies)
        graph.update(override_dependencies)
        if not extra.regular:
            return func(parsed, graph)
        args = {dependency: graph[dependency]
                for dependency in extra.dependencies}
        args.update(parsed)
        del args['__caparg_subcommand__']
        return func(**args)

    def dependency(self,
                   name=None,
                   dependencies=pyrsistent.v(),
                   possible_dependencies=pyrsistent.v(),
                   regular=False):
        """
        Register as a dependency.

        """
        glue = (dependencies, possible_dependencies, regular)
        transform = gather.Wrapper.glue(glue)
        ret = self._collector.register(name, transform=transform)
        return ret

    # Recursive implementation for now
    def mkgraph(self, things):
        """
        Resolve dependencies and generate them

        """
        collection = self._collector.collect()
        ret = {}

        def _build(thing, on_route=pyrsistent.s()):
            if thing in on_route:
                raise ValueError("circular dependency detected",
                                 thing, on_route)
            if thing in ret:
                return ret[thing]
            on_route = on_route.add(thing)
            plugin = collection[thing]
            func = plugin.original
            dependencies, possible_dependencies, regular = plugin.extra
            my_dependencies, my_possible_dependencies = {}, {}
            for other_thing in dependencies:
                my_dependencies[other_thing] = _build(other_thing, on_route)
            for other_thing in possible_dependencies:
                builder = functools.partial(_build, other_thing, on_route)
                my_possible_dependencies[other_thing] = builder
            if regular:
                args = {'build_' + key: value
                        for key, value in my_possible_dependencies.items()}
                args.update(my_dependencies)
                ret[thing] = func(**args)
            else:
                ret[thing] = func(my_dependencies, my_possible_dependencies)
            return ret[thing]
        for thing in things:
            _build(thing)
        return ret
