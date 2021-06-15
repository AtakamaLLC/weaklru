import gc

import pytest

from weaklru import WeakLRU

class Obj(str):
    pass

def test_set_get():
    l = WeakLRU(3)
    x = Obj("x")
    y = Obj("y")
    z = Obj("z")

    l.set(1, x)
    l.set(2, y)
    l.set(3, z)
    assert l.get(1) is x
    assert l.get(2) is y
    assert l.get(3) is z
    assert l.get(4, 5) == 5

    l.set(4, Obj("4"))
    l.set(5, Obj("5"))
    l.set(6, Obj("6"))
    l.set(7, Obj("7"))  # pushes out 4

    assert l.get(1) is x
    del x
    gc.collect()
    assert l.get(1) is None     # weak-collection
    assert l.get(4) is None

    assert l.get(5) == "5"
    assert l.get(6) == "6"
    assert l.peek(7) == "7"     # doesn't move 7 to the front

    l.set(2, y)

    assert l.peek(7) is None

    del l[6]

    assert l.peek(6) is None

    # doesn't raise... doesn't make sense too, for lru or weak
    with pytest.raises(KeyError):
        del l[6]
