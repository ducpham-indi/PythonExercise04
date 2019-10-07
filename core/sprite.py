from __future__ import annotations

import pygame
import core.game
from typing import *


class Rect():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Image:

    _image = None
    _rect = None

    def __init__(self, path: str):
        self._image = pygame.image.load(path)
        self._rect = self._image.get_rect()
        pass

    def move(self, dir: typing.Tuple[int, int]):
        self._rect.x += dir[0]
        self._rect.y += dir[1]

    def draw(self, game: core.game.Game):
        game.screen.blit(self._image, self._rect)

    @property
    def image(self):
        return self._image


class Sprite(pygame.sprite.Sprite):

    def __init__(self, path: str):
        super().__init__()
        self.image = Image(path).image
        self.rect = self.image.get_rect()
        pass

    def move(self, dir: typing.Tuple[int, int]):
        self.rect.x += dir[0]
        self.rect.y += dir[1]
        pass
