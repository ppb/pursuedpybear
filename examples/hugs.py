#!/usr/bin/env python3
"""
Select your monster by clicking on it.

Click and hold the mouse to move the monster.

Try to hug all the people by getting close to them.
"""
import ppb
import math
import time
import random
from ppb_mutant import MutantSprite
from utils import (
    CircularRegion, CircularMenuScene, AnimationSprite, MenuSprite,
    clamp,
)


print(__doc__)


class MotionMixin:
    target: ppb.Vector = None
    velocity: ppb.Vector = None
    max_speed: float = None

    def on_update(self, update, signal):
        if self.target is not None:
            if self.max_speed is None:
                self.position = self.target
            else:
                delta = (self.target - self.position)
                # Calculate the maximum amount we could travel in this time, and
                # limit to that.
                delta = delta.truncate(self.max_speed * update.time_delta)
                self.position += delta
        elif self.velocity is not None:
            v = self.velocity
            if self.max_speed is not None:
                v = v.truncate(self.max_speed)
            self.position += v * update.time_delta

        camera = update.scene.main_camera
        self.position = ppb.Vector(clamp(camera.frame_left, self.position.x, camera.frame_right),
                                   clamp(camera.frame_top, self.position.y, camera.frame_bottom),
        )

def sign(x):
    from math import copysign
    return copysign(1, x)

class RunnerSprite(MotionMixin, MutantSprite, CircularRegion):
    scared: bool = False
    scare_distance: float = 1.5
    relax_distance: float = 1.5 * scare_distance

    @property
    def emoji(self):
        if self.scared:
            return 'expressions/smileys/shock_fear_exhaustion/scared'
        else:
            return 'expressions/smileys/shock_fear_exhaustion/worried'

    @property
    def max_speed(self):
        scared_speed = 1
        if self.scared:
            return scared_speed
        else:
            return 0.9 * scared_speed

    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        self.velocity = ppb.Vector(0, 1).rotate(
            random.uniform(-180, 180)
        )

    def _check_bear(self, bear):
        # Use a Schmitt trigger to avoid oscillating behaviour
        d = (self.position - bear.position).length
        if d < self.scare_distance:
            self.scared = True
        elif d > self.relax_distance:
            self.scared = False

    def _check_walls(self, camera):
        # TODO: Do something gentler
        if not (camera.frame_left < self.position.x < camera.frame_right):
            if sign(camera.position.x - self.position.x) != sign(self.velocity.x):
                self.velocity = self.velocity.reflect(ppb.Vector(1, 0))

        if not (camera.frame_top < self.position.y < camera.frame_bottom):
            if sign(camera.position.y - self.position.y) != sign(self.velocity.y):
                self.velocity = self.velocity.reflect(ppb.Vector(0, 1))

    def _direction(self, bear, time_delta):
        max_angle = 360 * time_delta # Max. 1 turn per second
        rot = random.triangular(-max_angle, +max_angle)
        if self.scared:
            d = self.position - bear.position
            rot += self.velocity.angle(d)
            rot = clamp(-max_angle, rot, max_angle)

        self.velocity = self.velocity.rotate(rot).scale(self.max_speed)

    def on_update(self, update, signal):
        self._check_bear(update.scene.player)
        self._direction(update.scene.player, update.time_delta)
        self._check_walls(update.scene.main_camera)

        super().on_update(update, signal)


class HuggedSprite(MutantSprite, CircularRegion):
    emoji = 'expressions/smileys/embarrassed_affection/smile_hearts'


class HeartAnimSprite(MutantSprite, AnimationSprite):
    emoji = 'symbols/hearts/red_heart'

    line = ppb.Vector(0, -1)
    duration = 1

    def do_start(self, signal):
        self.position = self.aposition

    def do_frame(self, dt, t, signal):
        self.position = self.line * (t / self.duration) + self.aposition
        return t < self.duration


class PlayerSprite(MotionMixin, MutantSprite, CircularRegion):
    max_speed = 1.5

    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        self.target = None
        self.velocity = ppb.Vector(0, 0)

    def on_button_pressed(self, mouse, signal):
        if mouse.button is ppb.buttons.Primary:
            self.target = mouse.position

    def on_button_released(self, mouse, signal):
        if mouse.button is ppb.buttons.Primary:
            self.target = None

    def on_mouse_motion(self, mouse, signal):
        if ppb.buttons.Primary in mouse.buttons:
            self.target = mouse.position

    def on_update(self, update, signal):
        from math import inf, tanh
        super().on_update(update, signal)

        weight = sum(
            1 / (runner.position - self.position).length
            for runner in update.scene.get(kind=RunnerSprite)
            if runner.scared
        )

        base_speed = 1.5
        real_speed = 3
        self.max_speed = base_speed + (real_speed - base_speed) * tanh(weight)


class AISprite(PlayerSprite):
    emoji = 'robot'

    def intercept(self, other):
        δ = other.position - self.position
        v_H = other.velocity

        # Calling B and H the bear's and human's initial positions, t and I
        # the time and position of intercept, s the bear's speed, we have:
        # |BI| = t*s = |δ + t*v_H|; square to get a polynomial equation
        # a t² + 2 b t + c
        a = v_H * v_H - self.max_speed * self.max_speed
        b, c = δ * v_H, δ * δ
        Δ = b*b - a*c
        if Δ < 0:
            # Intercept is impossible
            return None

        t = min(filter(lambda t: t >= 0,
                       ((- b - math.sqrt(Δ))/a, (- b + math.sqrt(Δ))/a)))

        return other.position + t * other.velocity

    def on_update(self, update, signal):
        """Automatically steer the bear towards the closest hooman."""
        super().on_update(update, signal)

        targets = map(self.intercept, update.scene.get(kind=RunnerSprite))
        self.target = min(
            targets,
            key=lambda p: (p - self.position).length,
            default=None,
        )


class MainScene(ppb.BaseScene):
    runner_count = 10

    def __init__(self, *p, player=None, **kw):
        super().__init__(*p, background_color=(0, 100, 0), **kw)

        for _ in range(self.runner_count):
            self.add(RunnerSprite(pos=(
                random.uniform(self.main_camera.frame_left, self.main_camera.frame_right),
                random.uniform(self.main_camera.frame_top, self.main_camera.frame_bottom),
            )))
        self.player = player if player is not None else PlayerSprite()
        self.add(self.player)

    def hug(self, runner):
        hugged = HuggedSprite(pos=runner.position)
        self.remove(runner)
        self.add(hugged)
        self.add(HeartAnimSprite(anchor=hugged))

    def on_update(self, update, signal):
        bear = next(self.get(kind=PlayerSprite))
        count = 0
        for runner in self.get(kind=RunnerSprite):
            count += 1
            if bear.contains(runner):
                self.hug(runner)

        if not count:
            signal(ppb.events.Quit())


class CharacterSelectSprite(MutantSprite, CircularRegion, MenuSprite):
    def __init__(self, *p, emoji, **kw):
        super().__init__(*p, **kw)
        self.emoji = emoji


class CharacterSelectScene(CircularMenuScene):
    ring_increment = 1.25
    item_size = 1.25

    characters = [
        'puffer_fish',
        'owl',
        'coyote',
        'fox',
        'hyena',
        'jackal',
        'wolf',
        'troll',
        'oni',
        'goblin',
        'dark_elf',
        'minotaur',
        'orc',
        'bugbear',
        'demon',
        'elf',
        'kobold',
        'half_demon',
        'fish_person',
        'tiger',
        'cheetah',
        'lion_with_mane',
        'lion_without_mane',
        'jaguar',
        'leopard',
        'lynx',
        'snow_leopard',
        'slime',
        'deer_without_antlers',
        'bear',
        'raccoon',
        'mouse',
        'ram',
        'opossum',
        'rat',
        'rabbit',
        'red_panda',
        'panda',
        'deer_with_antlers',
        'otter',
        'snake',
        'frankensteins_monster',
        'clown',
        'tengu_mask',
        'robot',
        'alien_monster',
        'alien',
    ]

    def get_options(self):
        for e in self.characters:
            yield CharacterSelectSprite(emoji=e)

    def do_select(self, sprite, signal):
            # FIXME: Better way to send this data?
            PlayerSprite.emoji = sprite.emoji
            self.next = MainScene
            self.running = False


def auto():
    with ppb.GameEngine(MainScene, scene_kwargs={'player': AISprite()}) as engine:
        engine.start()  # Vrooom!
        stats = engine.main_loop(collect_statistics=True)

    with open('hugs_stats.feather', 'wb') as file:
        stats.to_feather(file)


def main():
    return ppb.run(
        starting_scene=CharacterSelectScene,
        # resolution=(700, 700),
        # window_title='Hug the Humans!',
    )


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2 and argv[1] == "auto":
        auto()
    else:
        main()
