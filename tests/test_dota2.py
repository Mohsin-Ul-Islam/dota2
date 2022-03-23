"""Test suite for dota2."""

from expects import be, equal, expect

from dota2 import __version__
from dota2.domain.models import Damage


def test_version():
    """Assert that the package version is correct."""

    expect(__version__).to(equal("0.1.0"))


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
