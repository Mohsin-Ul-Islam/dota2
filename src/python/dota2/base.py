from abc import ABC, abstractmethod

from dota2.clock import Clock


class Tickable(ABC):
    @abstractmethod
    def tick(self, clock: Clock) -> None:
        raise NotImplementedError()


class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError()
