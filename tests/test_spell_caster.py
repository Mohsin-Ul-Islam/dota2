"""Test suite for `SpellCaster`"""

from expects import equal, expect
from pytest import raises

from dota2.clock import MockClock
from dota2.mixins import SpellCaster


def test_spell_caster_mana_init():
    """SpellCaster's mana cannot be negative or greater than pool."""

    with raises(ValueError, match="mana cannot be negative"):
        SpellCaster(
            mana=-80,
            mana_pool=640,
            mana_regeneration_rate=2,
        )

    with raises(ValueError, match="mana cannot be greater than mana_pool"):
        SpellCaster(
            mana=700,
            mana_pool=640,
            mana_regeneration_rate=2,
        )


def test_spell_caster_mana_pool_init():
    """SpellCaster's mana_pool cannot be negative."""

    with raises(ValueError, match="mana_pool cannot be negative"):
        SpellCaster(
            mana=80,
            mana_pool=-640,
            mana_regeneration_rate=2,
        )


def test_spell_caster_mana_regen_rate_init():
    """SpellCaster's mana_regeneration_rate cannot be negative."""

    with raises(ValueError, match="mana_regeneration_rate cannot be negative"):
        SpellCaster(
            mana=80,
            mana_pool=640,
            mana_regeneration_rate=-2,
        )


def test_spell_caster_mana_regeneration():
    """SpellCaster can regenerate mana overtime."""

    clock = MockClock()
    dragon_knight = SpellCaster(
        mana=760,
        mana_pool=1500,
        mana_regeneration_rate=4,
    )

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.mana).to(equal(760))

    clock.advance(seconds=3)

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.mana).to(equal(772))


def test_spell_caster_max_mana_regeneration():
    """SpellCaster cannot regenerate mana more than mana pool."""

    clock = MockClock()
    dragon_knight = SpellCaster(
        mana=1490,
        mana_pool=1500,
        mana_regeneration_rate=4,
    )

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.mana).to(equal(1490))

    clock.advance(seconds=5)

    dragon_knight.tick(clock=clock)
    expect(dragon_knight.mana).to(equal(1500))
