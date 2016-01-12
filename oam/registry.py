#!/usr/bin/python

import logging
import unittest

class Registry:

    def __init__(self):
        self.catalog = {}
        self.logger = logging.getLogger("oam.registry")

    def register(self, tag, obj):
        self.logger.log(logging.INFO, "register: %s", tag)
        self.catalog[tag] = obj

    def exists(self, tag):
        return tag in self.catalog

    def get(self, tag):
        self.logger.log(logging.INFO, "get: %s", tag)
        return self.catalog[tag]

    def create(self, tag, argv = None):
        self.logger.log(logging.INFO, "create: %s", tag)
        if isinstance(self.catalog[tag], Registry):
            return Registry()
        else:
            return self.catalog[tag].create(argv)

    def tags(self):
        return sorted(self.catalog.keys())

    def remove(self, tag):
        self.logger.log(logging.INFO, "remove: %s", tag)
        del self.catalog[tag]
        
class RegistryTestCase(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()

    def test_register(self):
        self.registry.register('atag', Registry())
        self.assertTrue(self.registry.exists('atag'), msg = 'tag missing from registry')
        self.registry.remove('atag')
        self.assertFalse(self.registry.exists('atag'), msg = 'tag present in registry')

    def test_get(self):
        an_obj = Registry()
        self.registry.register('obj', an_obj)
        self.assertIs(an_obj, self.registry.get('obj'))

    def test_create(self):
        self.registry.register('reg', Registry())
        self.assertIsInstance(self.registry.create('reg'), Registry, msg = 'Registry object not created')
        
    def test_tags(self):
        self.registry.register('a', int(1))
        self.registry.register('b', int(2))
        self.registry.register('c', int(3))
        self.assertListEqual(self.registry.tags(), ['a', 'b', 'c'])
                      
    def tearDown(self):
        del self.registry
                      
if __name__ == '__main__':
    unittest.main()
