import ppb

RESOLUTION = (1200, 900)


class Ball(ppb.Sprite):
    image = ppb.Circle(255, 255, 255)
    size = 1
    velocity = ppb.Vector(0, 0)

    def on_update(self, event, signal):
        camera = event.scene.main_camera
        reflect = ppb.Vector(0, 0)

        if self.left < camera.left:
            reflect += ppb.directions.Right

        if self.right > camera.right:
            reflect += ppb.directions.Left

        if self.top > camera.top:
            reflect += ppb.directions.Down

        if self.bottom < camera.bottom:
            reflect += ppb.directions.Up

        if reflect:
            self.velocity = self.velocity.reflect(reflect.normalize())
        self.position += self.velocity * event.time_delta


def setup(scene):
    scene.background_color = (0, 0, 0)
    scene.add(Ball(velocity=ppb.directions.UpAndLeft * 3))


ppb.run(setup, resolution=RESOLUTION, title="Hellow Window!")