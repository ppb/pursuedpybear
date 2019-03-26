from time import monotonic

from pytest import mark
from pytest import raises

import ppb.testutils as testutil
from ppb.events import Quit


@mark.parametrize("loop_count", range(1, 6))
def test_quitter(loop_count):
    quitter = testutil.Quitter(loop_count=loop_count)
    for _ in range(loop_count):
        for e in quitter.activate(None):  # Quitter doesn't need access to the engine, so we can pass None here.
            if isinstance(e, Quit):
                return
    raise AssertionError("Quitter did not raise a quit event.")


def test_failer_immediate():
    failer = testutil.Failer(fail=lambda e: True, message="Expected failure.")

    with raises(AssertionError):
        failer.activate(None)


def test_failer_timed():
    failer = testutil.Failer(fail=lambda e: False, message="Should time out", run_time=0.1)

    start_time = monotonic()

    while True:
        try:
            failer.activate(None)
        except AssertionError as e:
            if e.args[0] == "Test ran too long.":
                end_time = monotonic()
                break
            else:
                raise

    run_time = end_time - start_time

    assert abs(run_time - 0.1) <= 0.01
