from expects import equal, expect

from dota2.clock import MockClock
from dota2.debuffs import BlighStoneDebuff, SpiritVesselDebuff
from dota2.mixins import Attackable


def test_spirit_vessel_debuff() -> None:
    """Spirit vessel reduces attackable's health regen by 75% for the
    duration."""

    clock = MockClock()
    crystal_maiden = Attackable(
        health=320, health_pool=540, health_regeneration_rate=2, armour=1
    )
    debuff = SpiritVesselDebuff(target=crystal_maiden, duration=2)

    debuff.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(320.0))

    clock.advance(seconds=1)

    debuff.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(321.5))

    clock.reset()
    clock.advance(seconds=1)

    debuff.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(323.5))

    clock.reset()
    clock.advance(seconds=1)

    debuff.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(326))


def test_blight_stone_debuff() -> None:
    """Blight stone reduces attackable's armour by 2 for the duration."""

    clock = MockClock()
    crystal_maiden = Attackable(
        health=320, health_pool=540, health_regeneration_rate=2, armour=3.75
    )
    debuff = BlighStoneDebuff(target=crystal_maiden, duration=2)

    debuff.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(1.75))

    clock.advance(seconds=1)

    debuff.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(1.75))

    clock.reset()
    clock.advance(seconds=1)

    debuff.tick(clock=clock)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(3.75))
