from __future__ import annotations
import pygame
from typing import *


class Scene:

    game: Game
    screen = property(lambda self: self.game.screen)
    clock = property(lambda self: self.game.clock)

    # callback: Game, Event
    # tuple: callback, event_type, event_keyboard, event_mouse_button
    __EventCallback = Tuple[Callable[[Any, Any], None], int, int, int]
    __event_callbacks: Set[__EventCallback]
    __callbacks_registered: bool = False

    def __init__(self):
        self.init()
        self.__event_callbacks = set()
        self.__callbacks_registered = False
        pass

    def init(self):
        raise NotImplementedError
        pass

    def update(self, dt: float):
        raise NotImplementedError
        pass

    def render(self):
        raise NotImplementedError

    def _setupGame(self, game: Game):
        self.game = game
        if self.__callbacks_registered is False:
            self.__callbacks_registered = True
            self.__autoRegisterEventCallbacks()

    def registerEventCallback(self, callback: Callable[[Game, Any], None],
                              event_filter: int,
                              key_filter: int = -1, mouse_filter: int = -1):
        """
        Register the event callback here
        """
        print(self.__event_callbacks)
        self.__event_callbacks.add((callback, event_filter, key_filter, mouse_filter))

    def __autoRegisterEventCallbacks(self):
        names = [func for func in dir(self) if callable(getattr(self, func))]
        for name in names:
            method = getattr(self, name)
            if hasattr(method, "_callback_req_event") is False:
                continue
            self.registerEventCallback(method,
                                       method._callback_req_event,
                                       method._callback_req_key,
                                       method._callback_req_mouse)
        pass

    def _resolve_event_callbacks(self, event):
        for callback in self.__event_callbacks:
            (f, req_event, req_key, req_btn) = callback
            event_type = getattr(event, "type", -1)
            event_key = getattr(event, "key", -1)
            event_btn = getattr(event, "button", -1)

            if req_event != event_type:
                continue
            if req_key >= 0 and req_key != event_key:
                continue
            if req_btn >= 0 and req_btn != event_btn:
                continue
            f(event)


class Game:
    fps: float = 60
    screen: Any
    clock: Any
    __done: bool = True
    width: int = 480
    height: int = 720
    __scenes: List[Scene] = list()

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Simple PyGame")
        self.__done = False

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pass
    
    def start(self):
        """
        Start the game and init the coreloop
        """
        self.__done = False

        while not self.__done:
            self.clock.tick(self.fps)
            
            scene = self.currentScene
            if scene is not None:
                self.screen.fill((0, 0, 0))
                for event in pygame.event.get():
                    scene._resolve_event_callbacks(event)
                scene.update(self.deltaTime)
                scene.render()
            else:
                for event in pygame.event.get():
                    pass

            pygame.display.flip()

        pygame.quit()

    def pushScene(self, scene: Scene):
        scene._setupGame(self)
        self.__scenes.insert(0, scene)

    def popScene(self) -> Scene:
        if len(self.__scenes) <= 0:
            return None
        return self.__scenes.pop(0)

    def getCurrentScene(self) -> Scene:
        if len(self.__scenes) <= 0:
            return None
        return self.__scenes[0]

    currentScene: Scene = property(getCurrentScene)

    def finish(self):
        self.__done = True

    @property
    def done(self) -> bool:
        """
        Return true if the game is done and terminated.
        By default this property is false unless the game is started
        with Start()
        """
        return self.__done

    @property
    def deltaTime(self) -> float:
        return self.clock.get_time() / 1000.0
        pass


def callback(event_filter: int, key_filter: int = -1, mouse_filter: int = -1):
    def deco(f):
        f._callback_req_event = event_filter
        f._callback_req_key = key_filter
        f._callback_req_mouse = mouse_filter
        return f
    return deco
