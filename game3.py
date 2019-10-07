from define.color import *
import pygame

import core.game
import core.text


class Scene1(core.game.Scene):

    scene2: core.game.Scene
    text: core.text.Text

    def init(self):
        self.scene2 = Scene2()
        self.text = core.text.Text("resources/Bungee.ttf", "ENTER TO GO TO SCENE 2")
        pass

    def update(self, dt: float):
        pass
    
    def render(self):
        self.text.draw(self.game, (240, 320))
        pass

    @core.game.callback(pygame.KEYDOWN, key_filter=pygame.K_ESCAPE)
    def onQuit(self, event):
        self.game.finish()
        pass

    @core.game.callback(pygame.KEYDOWN, key_filter=pygame.K_RETURN)
    def onGoToScene2(self, event):
        self.game.pushScene(self.scene2)
        pass


class Scene2(core.game.Scene):

    text: core.text.Text = None

    def init(self):
        self.text = core.text.Text("resources/Bungee.ttf", "ESCAPE TO GO TO SCENE 1")
        pass

    def update(self, dt: float):
        pass
    
    def render(self):
        self.text.draw(self.game, (240, 320))
        pass

    @core.game.callback(pygame.KEYDOWN, key_filter=pygame.K_ESCAPE)
    def onBackToScene1(self, event):
        self.game.popScene()
        pass


def run():
    game = core.game.Game()
    game.pushScene(Scene1())

    game.start()
