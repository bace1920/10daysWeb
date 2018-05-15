# -*- coding: ' utf-8 -*-
import unittest
import sys
sys.path.append("..")

from tendaysweb.app import Rule


def empty():
    pass


method = 'GET'


class TestRuleMatch(unittest.TestCase):
    def test_single_var(self):
        r: Rule = Rule('/<name>', [method], empty)
        self.assertTrue(r.match('/test', method))
        self.assertFalse(r.match('/api/test', method))


if __name__ == '__main__':
    unittest.main()