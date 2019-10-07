import pygame
import pygame.freetype
import core.game
import typing

_defaultFont = None
_fontCache = dict()


# TODO: cache font for reusability
class Text:

    Color = typing.Tuple[float, float, float]

    font = None
    __text: str = ""
    __color: Color = (255, 255, 255)
    __size: float = 20
    pos: typing.Tuple[float, float] = (0, 0)
    tex = None  # rendering texture
    rect = (0, 0, 0, 0)  # rendering rect

    def __init__(self, path: str, text: str = "", color: Color = (255, 255, 255), size: float = 20):
        global _defaultFont
        global _fontCache

        self.text = text
        self.color = color
        self.size = 20

        if path is None:
            if _defaultFont is None:
                _defaultFont = pygame.freetype.Font(None, self.__size)
            self.font = _defaultFont
        elif path in _fontCache:
            self.font = _fontCache[path]
        else:
            font = pygame.freetype.Font(path, self.__size)
            font.antialiased = True
            _fontCache[path] = font
            self.font = _fontCache[path]

    def setText(self, text: str):
        self.__text = text
        self.tex = None

    def setColor(self, color: Color):
        self.__color = color
        self.tex = None

    def setSize(self, size: float):
        self.__size = size
        self.tex = None

    text = property(lambda self: self.__text, setText)
    color = property(lambda self: self.__color, setColor)
    size = property(lambda self: self.__size, setSize)

    def draw(self, game: core.game.Game, pos: typing.Tuple[float, float] = None):

        if pos is not None:
            self.pos = pos

        if self.tex is None:
            self.tex, self.rect = self.font.render(self.text, self.color, size=self.size)

        (x, y) = (self.pos[0] - self.rect.width / 2, self.pos[1] - self.rect.height / 2)
        game.screen.blit(self.tex, (x, y))
