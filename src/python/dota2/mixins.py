from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from dota2.clock import Clock
from dota2.damage import Damage


class Tickable(ABC):
    @abstractmethod
    def tick(self, clock: Clock) -> None:
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

        if self.health < 0 or self.health_pool < 0 or self.health_regeneration_rate < 0:
            raise ValueError(
                "health, health_pool & health_regeneration_rate cannot be negative"
            )

        self.effective_health_regen_rate = self.health_regeneration_rate

    def deal(self, damage: Damage) -> None:
        """Deal damage to the attackable."""
        self.health = max(0, self.health - damage.value)

    def tick(self, clock: Clock) -> None:
        self.health = min(
            self.health_pool,
            self.health + clock.elapsed() * self.effective_health_regen_rate,
        )


@dataclass
class Movable(Tickable):
    movement_speed: float

    def tick(self, clock: Clock) -> None:
        pass
