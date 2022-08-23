from dataclasses import dataclass, field
from enum import Enum
from typing import Set

from dota2.base import Tickable
from dota2.clock import Clock
from dota2.damage import Damage

# from dota2.spells import Castable
from dota2.utils import Point3D, logger


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
class Spell(Tickable):
    mana: float
    health: float
    cooldown: float
    # target: Castable | None = field(default=None)
    cooldown_left: float = field(init=False, default=0)

    def tick(self, clock: Clock) -> None:

        self.cooldown_left = min(0, self.cooldown_left - clock.elapsed())
        if self.is_on_cooldown():
            return

    # def set_target(self, target: Castable) -> None:
    #     self.target = target

    def is_on_cooldown(self) -> bool:
        return self.cooldown_left > 0

    def is_not_on_cooldown(self) -> bool:
        return not self.is_on_cooldown()


@dataclass
class SpellCaster(Tickable):
    """An object that can cast active spells."""

    mana: float
    mana_pool: float
    mana_regeneration_rate: float

    # spells: Dict[Type[Spell], Spell] = field(default_factory=dict)

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

        # for spell in self.spells.values():
        #     spell.tick(clock=clock)

    # def cast(self, spell: Type[Spell], target: Castable) -> None:

    #     spell_ = self.spells[spell]
    #     if self.mana >= spell_.mana and spell_.is_not_on_cooldown():
    #         spell_.set_target(target)
    #         self.mana -= spell_.mana


@dataclass
class StatusEffectable:
    """An object that can have status effects."""

    class Effect(Enum):
        """Enumeration of status effects."""

        STUN = "STUN"
        MUTE = "MUTE"
        ROOT = "ROOT"
        BREAK = "BREAK"
        SILENCE = "SILENCE"

    resistence: float = field(default=0)
    effects: Set[Effect] = field(default_factory=set)

    def add_effect(self, effect: Effect) -> None:
        """Add status effect to the target."""
        self.effects.add(effect)

    def remove_effect(self, effect: Effect) -> None:
        """Remove a status effect from target."""
        self.effects.remove(effect)

    def is_silenced(self) -> bool:
        """Is the target silenced?"""
        return StatusEffectable.Effect.SILENCE in self.effects

    def is_stunned(self) -> bool:
        """Is the target stunned?"""
        return StatusEffectable.Effect.STUN in self.effects

    def is_broken(self) -> bool:
        """Is the target broken?"""
        return StatusEffectable.Effect.BREAK in self.effects

    def is_rooted(self) -> bool:
        """Is the target rooted?"""
        return StatusEffectable.Effect.ROOT in self.effects

    def is_muted(self) -> bool:
        """Is the target muted?"""
        return StatusEffectable.Effect.MUTE in self.effects
