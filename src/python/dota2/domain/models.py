"""Domain models for dota2."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass
class Damage:
    """The damage instance data class."""

    class Type(Enum):
        """Damage instance type.

        Can be one of `Physical`, `Magical` or `Pure`.
        """

        PHYSICAL = 0
        MAGICAL = 1
        PURE = 2

    value: float
    type_: Type

    @property
    def is_magical(self) -> bool:
        """Is the damage instance magical?"""
        return self.type_ == Damage.Type.MAGICAL

    @property
    def is_physical(self) -> bool:
        """Is the damage instance physical?"""
        return self.type_ == Damage.Type.PHYSICAL

    @property
    def is_pure(self) -> bool:
        """Is the damage instance pure?"""
        return self.type_ == Damage.Type.PURE


@dataclass
class Attackable:
    """An object that can be attacked."""

    health: float

    def deal(self, damage: Damage) -> None:
        """Deal damage to the attackable."""
        self.health = max(0, self.health - damage.value)
