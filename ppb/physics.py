def check_circle_collision(sprite1, sprite2):
    """
    Check two sprites using circle collision.

    :param sprite1:
    :param sprite2: Sprite must have a pos and radius.
    :return: bool: True if colliding.
    """
    return len(sprite1.pos - sprite2.pos) <= sprite1.radius + sprite2.radius


def collision_check(sprite1, sprite2, check=check_circle_collision):
    """
    Check collision between two sprites.

    :param sprite1
    :param sprite2: A sprite must have a pos and attributes needed by the
                    check function.
    :param check: A function that takes two sprites and returns bool
    :return: bool
    """
    return check(sprite1, sprite2)