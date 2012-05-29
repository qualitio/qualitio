# -*- coding: utf-8 -*-

# just to make sure I'm importing all utils from the same place
from django.utils.datastructures import SortedDict
from django.core.exceptions import ImproperlyConfigured

# alias
OrderedDict = SortedDict
del SortedDict


def comp(*func):
    """
    Composition of functions. Returns function, that will apply
    the result of the first function to the next one.

    >>> comp()(1)
    >>> 1
    >>>
    >>> comp(len)([1,2,3])
    >>> 3
    >>>
    >>> comp(sum, map)(len, [[1,2], [3], [5, 5]])  # === sum(map(len, [[1,2], [3], [5, 5]]))
    >>> 5
    """
    def invoker(*args, **kwargs):
        rev = list(reversed(func)) or [lambda x: x]
        result = rev.pop(0)(*args, **kwargs)
        for f in rev:
            result = f(result)
        return result
    return invoker


identity = lambda x: x
