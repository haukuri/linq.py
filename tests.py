from random import randint
import pytest

from linq import linq


def random_ints(length=100):
    return [randint(0, 10000) for _ in range(length)]


def test_linq_select():
    data = [1, 2]
    expected = [2, 4]
    actual = linq(data).select(lambda x: x * 2).to_list()
    assert actual == expected


def test_linq_where():
    data = [1, 2, 3, 4]
    expected = [2, 4]
    actual = linq(data).where(lambda x: x % 2 == 0).to_list()
    assert actual == expected


def test_linq_take():
    data = [1, 2, 3, 4]
    expected = [1, 2]
    actual = linq(data).take(2).to_list()
    assert actual == expected


def test_linq_skip():
    data = [1, 2, 3, 4]
    expected = [3, 4]
    actual = linq(data).skip(2).to_list()
    assert actual == expected


def test_select_many():
    data = [1, 2, 3]
    expected = [1, 1, 2, 2, 3, 3]
    actual = linq(data).select_many(lambda x: [x] * 2).to_list()
    assert actual == expected


def test_linq_iter():
    data = [1, 2, 3, 4]
    actual = list(x for x in linq(data))
    expected = data
    assert actual == expected


def test_linq_skip_while():
    data = [1, 2, 3, 4]
    actual = linq(data).skip_while(lambda x: x < 3).to_list()
    expected = [3, 4]
    assert actual == expected


def test_linq_contains():
    data = [1, 3, 4, 5]
    l = linq(data)
    assert all(l.contains(x) for x in data)


def test_linq_count():
    data = [1, 2, 3, 4]
    expected = 4
    actual = linq(data).count()
    assert actual == expected


def test_linq_to_dict():
    data = [(1, "a"), (2, "b")]
    expected = {1: "a", 2: "b"}
    actual = linq(data).to_dict(key=lambda x: x[0], value=lambda x: x[1])
    assert actual == expected


def test_linq_single_raises_value_error():
    data = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        linq(data).single()

