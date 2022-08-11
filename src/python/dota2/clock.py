"""Clock module for clockable dota2 classes."""

from dataclasses import dataclass


@dataclass
class MockClock:
    """Mock clock for testing clockable dota2 classes."""

    _start: int = 0
    _current: int = 0

    def forward(self, seconds: int) -> None:
        """Forwards the clock by given `seconds`"""
        self._current += abs(seconds)

    def reset(self) -> None:
        """Resets the clock."""
        self._current = self._start

    def elapsed(self) -> int:
        """Returns the elapsed time in seconds."""
        return self._current - self._start
