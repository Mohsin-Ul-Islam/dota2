"""Test suite for `Damage`."""

from expects import be, expect

from dota2.damage import Damage


def test_is_magical(
    magical_damage: Damage, physical_damage: Damage, pure_damage: Damage
):
    """Assert that is_magical damage instance returns correct boolean."""

    expect(magical_damage.is_magical).to(be(True))
    expect(physical_damage.is_magical).to(be(False))
    expect(pure_damage.is_magical).to(be(False))


def test_is_physical(
    magical_damage: Damage, physical_damage: Damage, pure_damage: Damage
):
    """Assert that is_physical damage instance returns correct boolean."""

    expect(magical_damage.is_physical).to(be(False))
    expect(physical_damage.is_physical).to(be(True))
    expect(pure_damage.is_magical).to(be(False))


def test_is_pure(magical_damage: Damage, physical_damage: Damage, pure_damage: Damage):
    """Assert that is_physical damage instance returns correct boolean."""

    expect(magical_damage.is_pure).to(be(False))
    expect(physical_damage.is_pure).to(be(False))
    expect(pure_damage.is_pure).to(be(True))
