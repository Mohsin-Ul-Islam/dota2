import logging
from dataclasses import dataclass

logger = logging.Logger(name="default", level=logging.DEBUG)
formatter = logging.Formatter("\x1b[38;5;39m[%(asctime)s] |\x1b[0m %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


@dataclass
class Point3D:
    x: float
    y: float
    z: float

    def __eq__(self, __o: object) -> bool:

        if not isinstance(__o, Point3D):
            return False

        if (
            round(__o.x) == round(self.x)
            and round(__o.y) == round(self.y)
            and round(__o.z) == round(self.z)
        ):
            return True

        return False
