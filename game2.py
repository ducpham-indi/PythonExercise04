import core.game
import core.sprite
import core.text
import pygame
from define.color import *


class Scene(core.game.Scene):

    sprites = None
    ball: core.sprite.Sprite = None
    text: core.text.Text
    x = 50
    y = 50

    def init(self):
        self.sprites = pygame.sprite.Group()
        self.ball = core.sprite.Sprite("resources/ball.png")
        self.text = core.text.Text("resources/Bungee.ttf")        

        self.text.text = "Hello world!"
        self.text.color = Color.GREEN
        self.text.defSize = 32

        print(self.text.text)

        self.text.pos = (160, 280)

        self.sprites.add(self.ball)
        pass

    def update(self, dt: float):
        pos = self.text.pos
        self.text.pos = (pos[0] + 20 * dt, pos[1])
        self.sprites.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.sprites.draw(self.game.screen)
        self.text.draw(self.game)
        pass

    @core.game.callback(pygame.KEYDOWN, key_filter=pygame.K_ESCAPE)
    def onQuit(self, event):
        self.finish()
        pass

    @core.game.callback(pygame.KEYDOWN)
    def onCursorMovement(self, event):
        if event.key == pygame.K_UP:
            self.ball.move((0, -10))
        if event.key == pygame.K_DOWN:
            self.ball.move((0, 10))
        if event.key == pygame.K_LEFT:
            self.ball.move((-10, 0))
        if event.key == pygame.K_RIGHT:
            self.ball.move((10, 0))


def run():
    game = core.game.Game()
    game.pushScene(Scene())
    game.start()
