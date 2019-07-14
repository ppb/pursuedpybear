from ppb.features.animation import Animation


def test_frames():
    time = 0

    def mockclock():
        nonlocal time
        return time

    class FakeAnimation(Animation):
        clock = mockclock

    anim = FakeAnimation("{2..5}", 1)

    assert [f.name for f in anim._frames] == ["2", "3", "4", "5"]

    time = 0
    assert anim.current_frame == 0

    time = 1
    assert anim.current_frame == 1

    time = 3
    assert anim.current_frame == 3

    time = 4
    assert anim.current_frame == 0


def test_pause():
    time = 0

    def mockclock():
        nonlocal time
        return time

    class FakeAnimation(Animation):
        clock = mockclock

    anim = FakeAnimation("{0..9}", 1)

    assert [f.name for f in anim._frames] == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    time = 0
    assert anim.current_frame == 0

    time = 5
    assert anim.current_frame == 5

    anim.pause()
    assert anim.current_frame == 5

    time = 12
    assert anim.current_frame == 5

    anim.unpause()
    assert anim.current_frame == 5

    time = 16
    assert anim.current_frame == 9

    time = 18
    assert anim.current_frame == 1


def test_filename():
    time = 0

    def mockclock():
        nonlocal time
        return time

    class FakeAnimation(Animation):
        clock = mockclock

    anim = FakeAnimation("spam{0..9}", 1)

    assert [f.name for f in anim._frames] == [
        "spam0", "spam1", "spam2", "spam3", "spam4", "spam5", "spam6", "spam7", "spam8", "spam9",
    ]

    anim.filename = 'eggs{0..4}'
    assert [f.name for f in anim._frames] == [
        "eggs0", "eggs1", "eggs2", "eggs3", "eggs4",
    ]
