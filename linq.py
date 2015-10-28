import itertools
from collections.abc import Sized


class linq:
    def __init__(self, iterable):
        assert iterable
        self.iterable = iterable

    def __iter__(self):
        yield from self.iterable

    def select(self, selector):
        return linq(selector(x) for x in self.iterable)

    def select_many(self, selector):
        it = (selector(x) for x in self.iterable)
        chained = itertools.chain.from_iterable(it)
        return linq(chained)

    def where(self, predicate):
        return linq(x for x in self.iterable if predicate(x))

    def take(self, n):
        it = itertools.islice(self.iterable, n)
        return linq(it)

    def skip(self, n):
        it = itertools.islice(self.iterable, n, None)
        return linq(it)

    def skip_while(self, predicate):
        def skipper():
            iterator = iter(self.iterable)
            while True:
                value = next(iterator)
                if not predicate(value):
                    yield value
                    break
            while True:
                yield next(iterator)
        return linq(x for x in skipper())

    def first(self):
        try:
            value = next(iter(self.iterable))
        except StopIteration:
            raise ValueError('first() called on an exhausted sequence')
        return value

    def first_or_none(self):
        try:
            return self.first()
        except ValueError:
            return None

    def single(self):
        li = self.to_list()
        if len(li) == 0:
            raise ValueError("single() called on an empty sequence")
        elif len(li) > 1:
            raise ValueError("single called on a s")
        return li[0]

    def single_or_none(self):
        try:
            return self.single()
        except ValueError:
            return None

    def to_list(self):
        if isinstance(self.iterable, list):
            return self.iterable
        return list(x for x in self)

    def to_set(self):
        return {x for x in self.iterable}

    def to_dict(self, key, value=None):
        if not value:
            return {key(x): x for x in self.iterable}
        return {key(x): value(x) for x in self.iterable}

    def all(self, predicate):
        return all(predicate(x) for x in self.iterable)

    def any(self, predicate):
        return any(predicate(x) for x in self.iterable)

    def __contains__(self, item):
        return item in self.iterable

    def contains(self, item):
        return item in self

    def __len__(self):
        if isinstance(self.iterable, Sized):
            return len(self.iterable)
        return sum(1 for _ in self.iterable)

    def count(self):
        return len(self)

    def distinct(self, key=None):
        if not key:
            return linq(self.to_set())
        return linq(self.to_dict(key=key).values())

    def group_by(self, key, value=None):
        it = itertools.groupby(self.iterable, key)
        return linq((k, linq(value(v) for v in vs)) for k, vs in it)

    def order_by(self, key=None):
        return linq(sorted(self.iterable, key=key))


def identity(x):
    return x
