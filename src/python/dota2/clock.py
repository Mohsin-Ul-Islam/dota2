"""Clock module for clockable dota2 classes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Clock(ABC):
    """Abstract Clock interface."""

    @abstractmethod
    def reset(self) -> None:
        """Resets the clock."""
        raise NotImplementedError()

    @abstractmethod
    def elapsed(self) -> int:
        """Returns the elapsed time in seconds."""
        raise NotImplementedError()


@dataclass
class MockClock(Clock):
    """Mock clock for testing clockable dota2 classes."""

    _start: int = 0
    _current: int = 0

    def advance(self, seconds: int) -> None:
        """Advances the clock by given `seconds`"""
        self._current += abs(seconds)

    def reset(self) -> None:
        """Resets the clock."""
        self._current = self._start

    def elapsed(self) -> int:
        """Returns the elapsed time in seconds."""
        return self._current - self._start
