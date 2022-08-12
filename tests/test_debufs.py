from expects import equal, expect

from dota2.clock import MockClock
from dota2.debufs import OrbOfCorrosionDebuf, SpiritVesselDebuf
from dota2.mixins import Attackable


def test_spirit_vessel_debuf() -> None:
    """Spirit vessel reduces attackable's health regen by 75% for the
    duration."""

    clock = MockClock()
    crystal_maiden = Attackable(
        health=320, health_pool=540, health_regeneration_rate=2, armour=1
    )
    debuf = SpiritVesselDebuf(target=crystal_maiden, duration=2)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(320.0))

    clock.advance(seconds=1)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(321.5))

    clock.reset()
    clock.advance(seconds=1)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(323))

    clock.reset()
    clock.advance(seconds=1)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(325))


def test_orb_of_corrosion_debuf() -> None:
    """Orb of corrosion reduces attackable's armour by 2 for the duration."""

    clock = MockClock()
    crystal_maiden = Attackable(
        health=320, health_pool=540, health_regeneration_rate=2, armour=3.75
    )
    debuf = OrbOfCorrosionDebuf(target=crystal_maiden, duration=2)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(1.75))

    clock.advance(seconds=1)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(1.75))

    clock.reset()
    clock.advance(seconds=1)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(1.75))

    clock.reset()
    clock.advance(seconds=1)

    debuf.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(3.75))
