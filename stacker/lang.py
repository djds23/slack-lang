# coding: utf-8
import re
from collections import deque
from functools import wraps

__all__ = ['Stacker', 'Procedure']

class Procedure (object):
    def __init__(self, inp):
        self.inp = inp

    def expression_list(self):
        return list(map(lambda s: s.strip(), self.inp[1:-1].split(';')))

class FuncMixin(object):
    def void_function(self, f):
        @wraps(f)
        def wrapper(*args):
            if any(args):
                raise StackerArgumentError('{} takes no arguments'
                                           ' but void'
                                           .format(f.__name__))
            return f(*args)
        return wrapper

class Stacker (FuncMixin):

    def __init__(self):
        self.STACK = deque()

    def stack_head(self):
        try:
            value = self.STACK[0]
        except IndexError:
            value = None
        return value

    def env(self, **kwargs):

        def _not(*args):
            value = self.STACK.popleft()
            if value is False:
                self.STACK.appendleft(True)
            else:
                self.STACK.appendleft(False)
            return self.STACK

        def _or (*args):
            value1 = self.STACK.popleft()
            value2 = self.STACK.popleft()
            if value1 is False and value2 is False:
                self.STACK.appendleft(False)
            else:
                self.STACK.appendleft(True)
            return self.STACK

        def _eq(*args):
            other = args[0]
            value = self.STACK.popleft()
            out = other == value
            self.STACK.appendleft(out)
            return self.STACK

        def rot(*args):
            value = self.STACK.popleft()
            self.STACK.append(value)
            return self.STACK

        def over(*args):
            value = self.stack_head()
            self.STACK.append(value)
            return self.STACK

        def drop(*args):
            self.STACK.popleft()
            return self.STACK

        def swap(*args):
            value1 = self.STACK.popleft()
            value2 = self.STACK.popleft()
            self.STACK.appendleft(value1)
            self.STACK.appendleft(value2)
            return self.STACK

        def dup(*args):
            value = self.stack_head()
            self.STACK.appendleft(value)
            return self.STACK

        def push(*args):
            self.STACK.appendleft(args[0])
            return self.STACK

        base = {
            'push': push,
            'drop': drop,
            'dup': dup,
            'swap': swap,
            'over': over,
            'rot': rot,
            'eq': _eq,
            'or': _or,
            'not': _not
        }

        if kwargs:
            base.update(kwargs)

        return base

    def parser(self, inp):
        if inp.startswith('{') and inp.endswith('}'):
            return Procedure(inp)
        if len(inp) == 0:
            return None
        funcs = '(' + '|'.join(self.env().keys()) + ')'
        matcher = re.compile('{} (\d+|\w+)'.format(funcs))
        expression = matcher.match(inp)
        if not expression:
            raise StackerSyntaxError('invalid syntax: {}'.format(inp))
        return [self.atomizer(atom) for atom in expression.group(0).split()]

    def atomizer(self, atom):
        try:
            value = int(atom)
        except ValueError:
            value = str(atom)
            if value == 'void':
                value = None

            if value == 'false':
                value = False

            if value == 'true':
                value = True

        return value

    def eval(self, inp):
        parsed_inp = self.parser(inp)
        if isinstance(parsed_inp, Procedure):
            for exp in parsed_inp.expression_list():
                atoms = self.parser(exp)
                self.eval_exp(atoms)
        else:
            self.eval_exp(parsed_inp)



    def eval_exp(self, atoms):
        if atoms is None:
            return None

        func = self.env().get(atoms[0], None)
        return func(*atoms[1:])

class StackerSyntaxError (Exception):
    pass

class StackerArgumentError (Exception):
    pass

class StackerTypeError (Exception):
    pass

class StackEatenUp (Exception):
    pass

