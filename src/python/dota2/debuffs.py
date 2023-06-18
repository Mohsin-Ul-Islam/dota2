from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List

from dota2.clock import Clock
from dota2.mixins import Attackable, Movable, StatusEffectable, Tickable
from dota2.utils import logger
from python.dota2.clock import Clock


@dataclass
class Debuff(Tickable):
    """Abstract base class for debuffs."""

    stackable: bool

    @abstractmethod
    def on_start(self) -> None:
        """Debuff lifecycle hook when the debuff is applied."""
        raise NotImplementedError()

    @abstractmethod
    def on_end(self) -> None:
        """Debuff lifecycle hook when the debuff ends."""
        raise NotImplementedError()

    @abstractmethod
    def is_expired(self) -> bool:
        """Is the debuff valid?"""
        raise NotImplementedError()

    @abstractmethod
    def reset(self) -> None:
        """Restart the debuff as if applied fresh."""
        raise NotImplementedError()


@dataclass
class Debuffable(Attackable):
    """An object that can be debuffed."""

    debuffs: List[Debuff] = field(default_factory=list)

    def add_debuff(self, debuff: Debuff) -> None:
        """Apply debuff on the target."""

        if debuff.stackable:
            debuff.on_start()
            return self.debuffs.append(debuff)

        for existing_debuff in self.debuffs:
            if isinstance(debuff, type(existing_debuff)):
                return existing_debuff.reset()

        debuff.on_start()
        self.debuffs.append(debuff)

    def tick(self, clock: Clock) -> None:
        for debuff in self.debuffs:
            debuff.tick(clock=clock)
            if debuff.is_expired():
                self.debuffs.remove(debuff)

        Attackable.tick(self, clock=clock)


@dataclass
class TimedDebuff(Debuff):
    """Debuff that live for a duration."""

    duration: float
    duration_left: float = field(init=False)

    def __post_init__(self) -> None:
        self.duration_left = self.duration

    def tick(self, clock: Clock) -> None:

        self.duration_left -= clock.elapsed()
        if self.is_expired():
            return self.on_end()

        self.on_tick()

    def is_expired(self) -> bool:
        return self.duration_left <= 0

    def reset(self) -> None:
        logger.debug(f"Debuff resets on {id(self)} to {self.duration}s")
        self.duration_left = self.duration

@dataclass
class ProximityDebuff(Debuff):
    """Debuff that works in a certain proximity"""

    proximity_radius: float

    def tick(self, clock: Clock) -> None:
        pass


@dataclass
class SpiritVesselDebuff(TimedDebuff):
    """Spirit vessel debuff."""

    target: Attackable
    _health_regen_change: float = field(init=False, default=0)

    def on_start(self) -> None:
        logger.debug(f"Applied spirit vessel on {id(self.target)} for {self.duration}s")
        self.on_tick()

    def on_end(self) -> None:
        logger.debug(f"Spirit vessel ends on {id(self.target)} after {self.duration}s")
        self.target.effective_health_regen_rate += self._health_regen_change

    def on_tick(self) -> None:

        if self._health_regen_change != self.target.health_regeneration_rate * 0.25:
            self._health_regen_change = self.target.health_regeneration_rate * 0.25
            self.target.effective_health_regen_rate -= self._health_regen_change


@dataclass
class BlighStoneDebuff(TimedDebuff):
    """Blight stone debuff."""

    target: Attackable
    _armour_change: float = field(init=False, default=2)

    def on_start(self) -> None:
        logger.debug(f"Applied blight stone to {id(self.target)} for {self.duration}s")
        self.target.armour -= self._armour_change

    def on_end(self) -> None:
        logger.debug(f"Blight stone ends on {id(self.target)} after {self.duration}s")
        self.target.armour += self._armour_change

    def on_tick(self) -> None:
        pass


@dataclass
class OrbOfVenomDebuff(TimedDebuff):
    """Orb of venom debuff."""

    target: Movable
    _move_speed_change: float = field(init=False)

    def on_start(self) -> None:
        self._move_speed_change = self.target.movement_speed * 0.13
        self.target.movement_speed -= self._move_speed_change

    def on_end(self) -> None:
        self.target.movement_speed += self._move_speed_change

    def on_tick(self) -> None:
        pass


@dataclass
class SilenceDebuff(TimedDebuff):
    """Silences a target for a given duration."""

    target: StatusEffectable

    def on_start(self) -> None:
        logger.debug(f"silenced {id(self)} for {self.duration}s")
        self.target.add_effect(StatusEffectable.Effect.SILENCE)

    def on_end(self) -> None:
        logger.debug(f"silence ended on {id(self)} after {self.duration}s")
        self.target.remove_effect(StatusEffectable.Effect.SILENCE)

    def on_tick(self) -> None:
        pass


@dataclass
class MuteDebuff(TimedDebuff):
    """Mutes a target for a given duration."""

    target: StatusEffectable

    def on_start(self) -> None:
        logger.debug(f"muted {id(self)} for {self.duration}s")
        self.target.add_effect(StatusEffectable.Effect.MUTE)

    def on_end(self) -> None:
        logger.debug(f"mute ended on {id(self)} after {self.duration}s")
        self.target.remove_effect(StatusEffectable.Effect.MUTE)

    def on_tick(self) -> None:
        pass


@dataclass
class StunDebuff(TimedDebuff):
    """Stuns a target for a given duration."""

    target: StatusEffectable

    def on_start(self) -> None:
        logger.debug(f"stunned {id(self)} for {self.duration}s")
        self.target.add_effect(StatusEffectable.Effect.STUN)

    def on_end(self) -> None:
        logger.debug(f"stun ended on {id(self)} after {self.duration}s")
        self.target.remove_effect(StatusEffectable.Effect.STUN)

    def on_tick(self) -> None:
        pass


@dataclass
class RadianceDebuff(ProximityDebuff):
    pass
