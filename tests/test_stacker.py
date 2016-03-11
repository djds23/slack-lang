from collections import deque

import unittest

from stacker.lang import Stacker


class TestStackerLangSpec(unittest.TestCase):

    def setUp(self):
        self.stacker = Stacker()
        self.assertEqual(self.stacker.STACK, deque([]))

    def test_push(self):
        self.stacker.eval('push 1', self.stacker.scope)
        self.stacker.eval('push 2', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([2, 1]))

    def test_swap(self):
        self.stacker.eval('push 1', self.stacker.scope)
        self.stacker.eval('push 2', self.stacker.scope)
        self.stacker.eval('swap void', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([1, 2]))

    def test_rot(self):
        self.stacker.eval('push 1', self.stacker.scope)
        self.stacker.eval('push 2', self.stacker.scope)
        self.stacker.eval('swap void', self.stacker.scope)
        self.stacker.eval('push 3', self.stacker.scope)
        self.stacker.eval('rot void', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([1, 2, 3]))

    def test_drop(self):
        self.stacker.eval('push 3', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([3]))
        self.stacker.eval('drop void', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([]))

    def test_over(self):
        self.stacker.eval('push 3', self.stacker.scope)
        self.stacker.eval('push 2', self.stacker.scope)
        self.stacker.eval('over void', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([2, 3, 2]))

    def test_eq(self):
        self.stacker.eval('push 100', self.stacker.scope)
        self.stacker.eval('eq 100', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([True]))

    def test_or(self):
        self.stacker.eval('push 100', self.stacker.scope)
        self.stacker.eval('eq 100', self.stacker.scope)

        self.stacker.eval('push 100', self.stacker.scope)
        self.stacker.eval('eq 99', self.stacker.scope)

        self.stacker.eval('or void', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([True]))

    def test_not(self):
        self.stacker.eval('push 100', self.stacker.scope)
        self.stacker.eval('eq 100', self.stacker.scope)
        self.stacker.eval('not void', self.stacker.scope)
        self.assertEqual(self.stacker.STACK, deque([False]))

    def test_code_block(self):
        self.stacker.eval(
            '{ push 9; drop void; push 9; eq 9;}',
            self.stacker.scope
        )

        self.assertEqual(self.stacker.STACK, deque([True]))


class TestImplementation(unittest.TestCase):

    def setUp(self):
        self.stacker = Stacker()
        self.assertEqual(self.stacker.STACK, deque([]))

    def test_env(self):
        env = self.stacker.env(new_arg=True)
        new_arg = env.get('new_arg', False)
        self.assertTrue(new_arg)



if __name__ == '__main__':
    unittest.main()

