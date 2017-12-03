from __future__ import print_function

import unittest

import elcaminoreal

from elcaminoreal.test import some_plugins

class DependencyResolverTester(unittest.TestCase):

    def test_mkgraph(self):
        result = some_plugins.COMMANDS.mkgraph(['bar'])
        self.assertEquals(result.pop('bar'), "I'm a bar")
        self.assertEquals(result, {})

    def test_mkgraph_cycle(self):
        with self.assertRaises(ValueError):
            some_plugins.COMMANDS.mkgraph(['robin'])

    def test_mkgraph_random(self):
        result = some_plugins.COMMANDS.mkgraph(['rand', 'needs_rand'])
        self.assertEquals(result['rand'], result['needs_rand']['rand'])

    def test_mkgraph_possible(self):
        result = some_plugins.COMMANDS.mkgraph(['foo_2'])
        self.assertEquals(result['foo_2'], dict(bar="I'm a bar"))

class RunnerResolverTester(unittest.TestCase):

    def test_run(self):
        output = []
        def my_print(*args):
            output.append(' '.join(map(str, args)))
        some_plugins.COMMANDS.run(['show', 'heee'],
                                   override_dependencies=dict(print=my_print))
        self.assertEquals(len(output), 1)
        args, deps = output[0].split(None, 1)
        self.assertIn('hee', args)
        self.assertIn('foo', deps)
        self.assertIn('bar', deps)
