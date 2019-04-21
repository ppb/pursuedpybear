from ppb.features.animation import Animation


def test_frames():
    time = 0

    def mockclock():
        nonlocal time
        return time

    class FakeAnimation(Animation):
        clock = mockclock

    anim = FakeAnimation("{2..5}", 1)

    time = 0
    assert anim.current_frame == 0
    assert str(anim) == '2'

    time = 1
    assert anim.current_frame == 1
    assert str(anim) == '3'

    time = 3
    assert anim.current_frame == 3
    assert str(anim) == '5'

    time = 4
    assert anim.current_frame == 0
    assert str(anim) == '2'


def test_pause():
    time = 0

    def mockclock():
        nonlocal time
        return time

    class FakeAnimation(Animation):
        clock = mockclock

    anim = FakeAnimation("{0..9}", 1)

    time = 0
    assert str(anim) == '0'

    time = 5
    assert str(anim) == '5'

    anim.pause()
    assert str(anim) == '5'

    time = 12
    assert str(anim) == '5'

    anim.unpause()
    assert str(anim) == '5'

    time = 16
    assert str(anim) == '9'

    time = 18
    assert str(anim) == '1'


def test_filename():
    time = 0

    def mockclock():
        nonlocal time
        return time

    class FakeAnimation(Animation):
        clock = mockclock

    anim = FakeAnimation("spam{0..9}", 1)

    time = 0
    assert str(anim) == 'spam0'

    time = 5
    assert str(anim) == 'spam5'

    anim.filename = 'eggs{0..4}'
    assert str(anim) == 'eggs0'

    time = 7
    assert str(anim) == 'eggs2'
