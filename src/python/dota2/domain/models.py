"""Domain models for dota2."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass
class Damage:
    """The damage instance data class."""

    class Type(Enum):
        """Damage instance type.

        Can be one of PHYSICAL or Magical
        """

        PHYSICAL = 0
        MAGICAL = 1

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
