from ppb.systems import Renderer


def test_calculate_new_size():
    renderer = Renderer()
    renderer.pixel_ratio = 80

    test_width = 240
    test_height = 160

    test_resolution = renderer.target_resolution(test_width, test_height, 1)
    assert test_resolution == (120, 80)

    test_width = 80
    test_height = 160

    test_resolution = renderer.target_resolution(test_width, test_height, 2)
    assert test_resolution == (160, 320)
