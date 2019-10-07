import core.game
import core.sprite
import pygame
from define.color import *


class Scene(core.game.Scene):

    ball: core.sprite.Image
    x = 50
    y = 50

    def init(self):
        self.ball = core.sprite.Image("resources/ball.png")
        pass
    
    def update(self, dt):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))
        self.ball.draw(self.game)
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
