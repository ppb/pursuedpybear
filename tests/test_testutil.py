from time import monotonic
from unittest.mock import Mock

from pytest import mark
from pytest import raises

import ppb.testutils as testutil
from ppb.events import Idle
from ppb.events import Quit


@mark.parametrize("loop_count", list(range(1, 6)))
def test_quitter(loop_count):
    quitter = testutil.Quitter(loop_count=loop_count)
    signal_mock = Mock()
    for i in range(loop_count):
        quitter.on_idle(Idle(.01), signal_mock)
    signal_mock.assert_called_once()
    assert len(signal_mock.call_args[0]) == 1
    assert len(signal_mock.call_args[1]) == 0
    assert isinstance(signal_mock.call_args[0][0], Quit)


def test_failer_immediate():
    failer = testutil.Failer(fail=lambda e: True, message="Expected failure.", engine=None)

    with raises(AssertionError):
        failer.on_idle(Idle(0.0), lambda x: None)


def test_failer_timed():
    failer = testutil.Failer(fail=lambda e: False, message="Should time out", run_time=0.1, engine=None)

    start_time = monotonic()

    while True:
        try:
            failer.on_idle(Idle(0.0), lambda x: None)
        except AssertionError as e:
            if e.args[0] == "Test ran too long.":
                end_time = monotonic()
                break
            else:
                raise

    run_time = end_time - start_time

    assert abs(run_time - 0.1) <= 0.011
