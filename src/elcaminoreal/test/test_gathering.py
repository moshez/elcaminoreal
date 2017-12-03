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
