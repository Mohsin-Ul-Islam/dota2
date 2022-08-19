from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from dota2.clock import Clock
from dota2.damage import Damage
from dota2.utils import Point3D, logger


class Tickable(ABC):
    @abstractmethod
    def tick(self, clock: Clock) -> None:
        raise NotImplementedError()


class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError()


@dataclass
class Attackable(Tickable):
    """An object that can be attacked."""

    health: float
    health_pool: float
    health_regeneration_rate: float

    armour: float
    effective_health_regen_rate: float = field(init=False)

    def __post_init__(self) -> None:

        if self.health < 0:
            raise ValueError("health cannot be negative")

        if self.health_pool < 0:
            raise ValueError("health_pool cannot be negative")

        if self.health_regeneration_rate < 0:
            raise ValueError("health_regeneration_rate cannot be negative")

        if self.health > self.health_pool:
            raise ValueError("health cannot be greater than health_pool")

        self.effective_health_regen_rate = self.health_regeneration_rate

    def deal(self, damage: Damage) -> None:
        """Deal damage to the attackable."""

        logger.debug(
            f"Dealt {damage.value} {damage.type_.name.lower()} damage to {id(self)}"
        )
        self.health = max(0, self.health - damage.value)

    def tick(self, clock: Clock) -> None:
        self.health = min(
            self.health_pool,
            self.health + clock.elapsed() * self.effective_health_regen_rate,
        )


@dataclass
class Movable(Tickable):
    movement_speed: float
    location: Point3D
    destination: Point3D = field(init=False)

    def __post_init__(self) -> None:
        self.destination = self.location

    def move_to(self, location: Point3D) -> None:
        self.destination = location

    def stop(self) -> None:
        self.destination = self.location

    def tick(self, clock: Clock) -> None:

        if self.location == self.destination:
            return

        elapsed = clock.elapsed()
        self.location.x = self.location.x + self.movement_speed * elapsed
        # self.location.y = self.location.y - self.movement_speed * elapsed


@dataclass
class SpellCaster(Tickable):
    """An object that can cast active spells."""

    mana: float
    mana_pool: float
    mana_regeneration_rate: float

    def __post_init__(self) -> None:

        if self.mana < 0:
            raise ValueError("mana cannot be negative")

        if self.mana_pool < 0:
            raise ValueError("mana_pool cannot be negative")

        if self.mana_regeneration_rate < 0:
            raise ValueError("mana_regeneration_rate cannot be negative")

        if self.mana > self.mana_pool:
            raise ValueError("mana cannot be greater than mana_pool")

    def tick(self, clock: Clock) -> None:
        self.mana = min(
            self.mana_pool,
            self.mana + clock.elapsed() * self.mana_regeneration_rate,
        )


@dataclass
class Hero(Attackable, SpellCaster):
    name: str

    def tick(self, clock: Clock) -> None:

        # we are explicity calling base class tick
        # instead of using super().tick because
        # we do not want to call super() in base
        # classes as they derive from an abstract base
        # called Tickable which raises NotImplemented in tick()
        # plus we define our own ordering instead of python's
        # inheritance MRO (method resolution ordering)
        Attackable.tick(self, clock)
        SpellCaster.tick(self, clock)
