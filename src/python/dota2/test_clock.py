"""Test suite for Mock Clock."""

from expects import be, expect

from dota2.clock import MockClock


def test_clock_elapsed() -> None:
    """Clock can return elapsed time in (seconds)"""

    clock = MockClock()
    expect(clock.elapsed()).to(be(0))


def test_clock_advance() -> None:
    """Clock can be advanceed by n seconds."""

    clock = MockClock()
    expect(clock.elapsed()).to(be(0))

    clock.advance(seconds=4)
    expect(clock.elapsed()).to(be(4))


def test_clock_reset() -> None:
    """Clock can be reset."""

    clock = MockClock()
    expect(clock.elapsed()).to(be(0))

    clock.advance(seconds=4)
    expect(clock.elapsed()).to(be(4))

    clock.reset()
    expect(clock.elapsed()).to(be(0))
