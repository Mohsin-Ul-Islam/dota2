"""Test suite for `Attackable`"""

from expects import equal, expect

from dota2.clock import MockClock
from dota2.damage import Damage
from dota2.mixins import Attackable


def test_can_deal_damage_to_attackable(physical_damage: Damage):
    """Attackable's health can be reduced by damage instance."""

    tier_one_tower = Attackable(
        health=1120.75,
        health_pool=1500,
        health_regeneration_rate=3.75,
        armour=1,
    )
    physical_damage.value = 120

    expect(tier_one_tower.health).to(equal(1120.75))
    tier_one_tower.deal(physical_damage)
    expect(tier_one_tower.health).to(equal(1000.75))


def test_attackable_health_cannot_get_negative(physical_damage: Damage):
    """Attackable's health can max go to zero."""

    tier_one_tower = Attackable(
        health=1120.75,
        health_pool=1500,
        health_regeneration_rate=3.75,
        armour=1,
    )
    physical_damage.value = 1500

    expect(tier_one_tower.health).to(equal(1120.75))
    tier_one_tower.deal(physical_damage)
    expect(tier_one_tower.health).to(equal(0))


def test_attackable_health_regeneration():
    """Attackable can regenerate health overtime."""

    clock = MockClock()
    dragon_knight = Attackable(
        health=760,
        health_pool=1500,
        health_regeneration_rate=4,
        armour=1,
    )

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.health).to(equal(760))

    clock.advance(seconds=3)

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.health).to(equal(772))


def test_attackable_max_health_regeneration():
    """Attackable cannot regenerate health more than health pool."""

    clock = MockClock()
    dragon_knight = Attackable(
        health=1490,
        health_pool=1500,
        health_regeneration_rate=4,
        armour=1,
    )

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.health).to(equal(1490))

    clock.advance(seconds=5)

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.health).to(equal(1500))
