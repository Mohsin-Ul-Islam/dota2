"""Test suite for `Attackable`"""

from expects import equal, expect

from dota2.domain.models import Attackable, Damage


def test_can_deal_damage_to_attackable(physical_damage: Damage):
    """Attackable's health can be reduced by damage instance."""

    tier_one_tower = Attackable(health=1120.75)
    physical_damage.value = 120

    expect(tier_one_tower.health).to(equal(1120.75))
    tier_one_tower.deal(physical_damage)
    expect(tier_one_tower.health).to(equal(1000.75))


def test_attackable_health_cannot_get_negative(physical_damage: Damage):
    """Attackable's health can max go to zero."""

    tier_one_tower = Attackable(health=1120.75)
    physical_damage.value = 1500

    expect(tier_one_tower.health).to(equal(1120.75))
    tier_one_tower.deal(physical_damage)
    expect(tier_one_tower.health).to(equal(0))
