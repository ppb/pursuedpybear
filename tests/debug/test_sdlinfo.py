import ppb.debug.sdlinfo as sdlinfo


# This mostly tests that it doesn't crash

def test_version():
    sdlinfo.sdl_version()


def test_revision():
    sdlinfo.sdl_revision()


def test_video_drivers():
    list(sdlinfo.iter_video_drivers())


# def test_check_video_driver():
#     sdlinfo.check_video_driver(...)


def test_render_drivers():
    list(sdlinfo.iter_render_drivers())


def test_audio_drivers():
    list(sdlinfo.iter_audio_drivers())


# def test_check_audio_driver():
#     sdlinfo.check_audio_driver(...)


def test_audio_codecs():
    list(sdlinfo.check_audio_codecs())


def test_image_codecs():
    list(sdlinfo.check_image_codecs())


def test_joysticks():
    list(sdlinfo.iter_joysticks())


# def test_haptics():
#     list(sdlinfo.iter_haptics())
