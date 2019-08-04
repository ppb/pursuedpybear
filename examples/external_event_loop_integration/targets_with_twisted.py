import logging
import ppb
from ppb import Vector
from ppb import keycodes
from twisted.internet import defer
from twisted.internet import task
from twisted.internet import endpoints
from twisted.web.server import Site
import klein
from dataclasses import dataclass
from typing import Any


class MoverMixin(ppb.BaseSprite):
    velocity = Vector(0, 0)

    def on_update(self, update, signal):
        self.position += self.velocity * update.time_delta


class Player(MoverMixin, ppb.BaseSprite):
    # We handle movement by mapping each key to a velocity vector
    # and adding it on press and subtracting it on release.
    left_vector = Vector(-1, 0)
    right_vector = Vector(1, 0)

    def on_key_pressed(self, event, signal):
        if event.key in (keycodes.A, keycodes.Left):
            self.velocity += self.left_vector
        elif event.key in (keycodes.D, keycodes.Right):
            self.velocity += self.right_vector
        elif event.key is keycodes.Space:
            self._fire_bullet(event.scene)

    def on_key_released(self, event, signal):
        if event.key in (keycodes.A, keycodes.Left):
            self.velocity -= self.left_vector
        elif event.key in (keycodes.D, keycodes.Right):
            self.velocity -= self.right_vector

    def on_button_pressed(self, event, signal):
        if event.button is ppb.buttons.Primary:
            self._fire_bullet(event.scene)

    def _fire_bullet(self, scene):
        scene.add(
            Bullet(pos=self.position),
            tags=['bullet']
        )


@dataclass(eq=False)
class TargetCounter(object):

    engine: Any

    app = klein.Klein()

    @app.route('/')
    def count(self, request):
        return str(len(list(self.engine.current_scene.get(tag='target'))))

    @classmethod
    def web_server(cls, reactor, engine, description):
        ep = endpoints.serverFromString(reactor, description)
        counter = cls(engine)
        return ep.listen(Site(counter.app.resource()))


class Bullet(MoverMixin, ppb.BaseSprite):
    velocity = Vector(0, 2)

    def on_update(self, update, signal):
        super().on_update(update, signal)  # Execute movement

        scene = update.scene
        
        if self.position.y > scene.main_camera.frame_bottom:
            scene.remove(self)
        else:
            for target in scene.get(tag='target'):
                d = (target.position - self.position).length
                if d <= target.radius:
                    scene.remove(self)
                    scene.remove(target)
                    break


class Target(ppb.BaseSprite):
    radius = 0.5


class GameScene(ppb.BaseScene):
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)

        # Set up sprites
        self.add(Player(pos=Vector(0, 0)), tags=['player'])

        # 5 targets in x = -3.75 -> 3.75, with margin
        for x in (-3, -1.5, 0, 1.5, 3):
            self.add(Target(pos=Vector(x, 1.875)), tags=['target'])


######### This is "non-game-specific code" ###########
class _FinishLoop(Exception):
    pass


@defer.inlineCallbacks
def twisted_engine_loop(engine):
    def loop_once(engine):
        if not engine.running:
            raise _FinishLoop(engine)
        engine.loop_once()
    loop = task.LoopingCall(loop_once, engine)
    engine.start()
    try:
        yield loop.start(0.001)
    except _FinishLoop:
        pass
######### End of "non-game-specific code" ###########


@defer.inlineCallbacks
def main(reactor):
    with ppb.make_engine(starting_scene=GameScene) as engine:
        TargetCounter.web_server(
            reactor=reactor,
            engine=engine,
            description="tcp:8080"
        )
        yield twisted_engine_loop(engine)

if __name__ == "__main__":
    import sys
    task.react(main, sys.argv[1:])
