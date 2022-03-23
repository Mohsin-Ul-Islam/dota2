"""root conftest file for pytest."""

from pytest import fixture

from dota2.domain.models import Damage


@fixture(scope="function")
def magical_damage() -> Damage:
    """Fixture to return default magical damage instance."""
    return Damage(47.32, Damage.Type.MAGICAL)


@fixture(scope="function")
def physical_damage() -> Damage:
    """Fixture to return default physical damage instance."""
    return Damage(35.17, Damage.Type.PHYSICAL)


@fixture(scope="function")
def pure_damage() -> Damage:
    """Fixture to return default pure damage instance."""
    return Damage(110.02, Damage.Type.PURE)
