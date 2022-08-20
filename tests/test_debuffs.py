from expects import equal, expect

from dota2.clock import MockClock
from dota2.debuffs import BlighStoneDebuff, Debuffable, SpiritVesselDebuff


def test_spirit_vessel_debuff() -> None:
    """Spirit vessel reduces attackable's health regen by 75% for the
    duration."""

    clock = MockClock()
    crystal_maiden = Debuffable(
        health=320, health_pool=540, health_regeneration_rate=2, armour=1
    )
    debuff = SpiritVesselDebuff(stackable=False, target=crystal_maiden, duration=2)
    crystal_maiden.add_debuff(debuff=debuff)

    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(320.0))

    clock.advance(seconds=1)

    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(321.5))

    clock.reset()
    clock.advance(seconds=1)

    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(323.5))

    clock.reset()
    clock.advance(seconds=1)

    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.health).to(equal(325.5))


def test_blight_stone_debuff() -> None:
    """Blight stone reduces attackable's armour by 2 for the duration."""

    clock = MockClock()
    crystal_maiden = Debuffable(
        health=320, health_pool=540, health_regeneration_rate=2, armour=3.75
    )
    debuff = BlighStoneDebuff(stackable=False, target=crystal_maiden, duration=2)

    crystal_maiden.add_debuff(debuff=debuff)
    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(1.75))

    clock.advance(seconds=1)

    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(1.75))

    clock.reset()
    clock.advance(seconds=1)

    crystal_maiden.tick(clock=clock)
    expect(crystal_maiden.armour).to(equal(3.75))


def test_blight_stone_should_not_stack():
    """Blight Stone should not stack on Attackable but refresh its timer."""

    clock = MockClock()
    ember_spirit = Debuffable(
        health=320, health_pool=540, health_regeneration_rate=2, armour=3.75
    )
    debuff = BlighStoneDebuff(stackable=False, target=ember_spirit, duration=2)
    non_stacking_debuff = BlighStoneDebuff(
        stackable=False, target=ember_spirit, duration=5
    )

    ember_spirit.add_debuff(debuff=debuff)
    ember_spirit.tick(clock=clock)
    expect(ember_spirit.armour).to(equal(1.75))
    expect(debuff.duration_left).to(equal(2))

    clock.advance(seconds=1)

    ember_spirit.tick(clock=clock)
    ember_spirit.add_debuff(debuff=non_stacking_debuff)
    expect(ember_spirit.armour).to(equal(1.75))
    expect(debuff.duration_left).to(equal(2))
