import functools


class Unique:
    """Singleton decorator which raise UserWarning if more than one instance is created"""

    _called = {}


    def __init__(self, cls):
        self._cls = cls
        functools.update_wrapper(self, cls)


    def __call__(self, *args, **kwargs):
        if self._cls in self._called:
            raise UserWarning(f" You used more than one instance of {self._cls.__name__}. Remove one")
        self._called[self._cls] = self._cls(*args, **kwargs)
        return self._called[self._cls]


    def __repr__(self):
        return self._called[self._cls].__repr__()

    def __doc__(self):
        return self._called[self._cls].__doc__()

    def __str__(self):
        return self._called[self._cls].__str__()

