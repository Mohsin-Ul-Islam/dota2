from dataclasses import dataclass, field

from dota2.clock import Clock
from dota2.debuffs import Debuffable
from dota2.mixins import SpellCaster, StatusEffectable


@dataclass
class Hero(StatusEffectable, Debuffable, SpellCaster):
    name: str = field(default="Unknown")

    def tick(self, clock: Clock) -> None:

        # we are explicity calling base class tick
        # instead of using super().tick because
        # we do not want to call super() in base
        # classes as they derive from an abstract base
        # called Tickable which raises NotImplemented in tick()
        # plus we define our own ordering instead of python's
        # inheritance MRO (method resolution ordering)
        Debuffable.tick(self, clock)
        SpellCaster.tick(self, clock)
