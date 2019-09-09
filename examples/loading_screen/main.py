from itertools import product

import ppb
from ppb.features import animation
from ppb.features import loadingscene


class LoadingSprite(ppb.Sprite):
    ready_image = ppb.Image("resources/load_bar/center_filled.png")
    waiting_image = ppb.Image("resources/load_bar/center_empty.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = self.waiting_image


class Game(ppb.BaseScene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wall_images = [
            ppb.Image(f"resources/terrain/wall_{x}.png")
            for x
            in range(1, 5)
        ]
        self.floor_images = [
            ppb.Image(f"resources/terrain/floor_{x}.png")
            for x in range(1, 5)
        ]
        self.blob_animation = animation.Animation("resources/blob/blob_{0..6}.png", 12)
        self.squares = [
            ppb.Image(f"resources/squares/sprite_{str(x).zfill(2)}.png")
            for x in range(60)
        ]

    def on_scene_started(self, scene_started: ppb.events.SceneStarted, signal):
        images = [*self.wall_images, *self.floor_images, self.blob_animation, *self.squares]
        for (x, y), image in zip(product(range(-5, 6), range(-3, 4)), images):
            self.add(ppb.Sprite(image=image, position=ppb.Vector(x, y)))


class LoadScreen(loadingscene.BaseLoadingScene):
    next_scene = Game

    def get_progress_sprites(self):
        left = LoadingSprite(
            position=ppb.Vector(-4, 0),
            ready_image=ppb.Image("resources/load_bar/left_filled.png"),
            waiting_image=ppb.Image("resources/load_bar/left_empty.png")
        )
        center = [LoadingSprite(position=ppb.Vector(x, 0)) for x in range(-3, 4)]
        right = LoadingSprite(
            position=ppb.Vector(4, 0),
            ready_image=ppb.Image("resources/load_bar/right_filled.png"),
            waiting_image=ppb.Image("resources/load_bar/right_empty.png")
        )
        return [left, *center, right]

    def update_progress(self, progress):
        bar = sorted(self.get(tag='progress'), key=lambda s: s.position.x)

        progress_index = progress * len(bar)

        for i, sprite in enumerate(bar):
            if i <= progress_index:
                sprite.image = sprite.ready_image
            else:
                sprite.image = sprite.waiting_image


ppb.run(starting_scene=LoadScreen)
