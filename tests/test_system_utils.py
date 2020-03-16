import gc

from ppb.systems._utils import ObjectSideData


def test_osd_basic():
    class Foo:
        pass

    myobj = Foo()

    osd = ObjectSideData()

    osd[myobj] = "foo"

    assert osd[myobj] == "foo"

    del myobj
    gc.collect()

    assert len(osd) == 0
