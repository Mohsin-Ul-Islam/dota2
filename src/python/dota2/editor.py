import random
import sys
from datetime import datetime

import pygame
from pygame.locals import *

from dota2.clock import Clock
from dota2.damage import Damage
from dota2.debuffs import BlighStoneDebuff, SpiritVesselDebuff
from dota2.mixins import Hero, Movable, Tickable
from dota2.utils import Point3D


class Animation(Tickable):
    def __init__(self, tileset, delay) -> None:
        self.tileset = tileset
        self.delay = delay
        self.time = 0
        self.tile = 0

    def reset(self) -> None:
        self.tile = 0

    def tick(self, clock: Clock) -> None:
        self.time += clock.elapsed()

        if self.time >= self.delay:
            self.tile = (self.tile + max(1, round(self.time / self.delay))) % len(
                self.tileset
            )
            self.time = 0

    def get_current_tile(self) -> pygame.Surface:
        return self.tileset[self.tile]


class PygameClock(Clock):
    def __init__(self) -> None:
        self.time = datetime.now()

    def reset(self) -> None:
        self.time = datetime.now()

    def elapsed(self) -> int:
        return (datetime.now() - self.time).total_seconds()


# initialize the pygame module
pygame.init()

# initialize the display module
pygame.display.init()

# display the font module
pygame.font.init()

screen_width = 1280
screen_height = 640

# set the display mode to 640 X 480 pixels
pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF)
pygame.display.set_caption("Dota 2")

# initialize the fps clock
fps_clock = pygame.time.Clock()

# initialize game clock
clock = PygameClock()


# load resources
character_tileset = pygame.image.load(
    "assets/images/character_tileset.png"
).convert_alpha()


# initialize variables
tile_width = 128
tile_height = 128

walking_tileset = []
standing_tileset = []

for i in range(8):
    surface = pygame.Surface((tile_width, tile_height))
    surface.blit(
        character_tileset,
        (0, 0),
        (i * tile_width, 0 * tile_height, tile_width, tile_height),
    )
    walking_tileset.append(surface)

for i in range(1):
    surface_ = pygame.Surface((tile_width, tile_height))
    surface_.blit(
        character_tileset,
        (0, 0),
        (i * tile_width, 0 * tile_height, tile_width, tile_height),
    )
    standing_tileset.append(surface_)

hero = Movable(1, Point3D(0, 2, 0))
dragon_knight = Hero(
    name="Dragon Knight",
    health=420,
    health_pool=740,
    health_regeneration_rate=2.3,
    armour=2,
    mana=173,
    mana_pool=230,
    mana_regeneration_rate=1.1,
)
walking_animation = Animation(tileset=walking_tileset, delay=0.1)
standing_animation = Animation(tileset=standing_tileset, delay=0.1)

hero_animation = standing_animation

# initialize default font with size of 16px
font = pygame.font.Font(pygame.font.get_default_font(), 14)

debuffs = []
heroes = [dragon_knight, hero]

# game loop
while True:

    # reset the game clock every loop
    clock.reset()

    # grap and process events from the event queue
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYUP and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_UP:
            hero.move_to(Point3D(7, 2, 0))
            standing_animation.reset()
            hero_animation = walking_animation
            # time.sleep(5)

        if event.type == KEYDOWN and event.key == K_DOWN:
            # walking_animation.reset()
            hero.stop()
            hero_animation = standing_animation

        if event.type == KEYDOWN and event.key == K_SPACE:
            dragon_knight.deal(
                Damage(value=random.randint(54, 72), type_=Damage.Type.PHYSICAL)
            )

        if event.type == KEYDOWN and event.key == K_s:
            debuffs.append(
                SpiritVesselDebuff(target=dragon_knight, duration=random.randint(1, 4))
            )

        if event.type == KEYDOWN and event.key == K_b:
            debuffs.append(
                BlighStoneDebuff(target=dragon_knight, duration=random.randint(2, 6))
            )

    # display surface
    display = pygame.display.get_surface()

    # clear the screen
    display.fill((0, 0, 0, 0))

    display.blit(
        hero_animation.get_current_tile(),
        (hero.location.x * tile_width, hero.location.y * tile_height),
    )

    # widget = HealthWidget(
    #     pos_x=screen_width / 2, pos_y=screen_height / 2, attackable=dragon_knight
    # )
    # display.blit(widget.surface(), (10, 10))

    health_ratio = dragon_knight.health / dragon_knight.health_pool * 100
    mana_ratio = dragon_knight.mana / dragon_knight.mana_pool * 100

    health_text = f"{round(dragon_knight.health)} / {dragon_knight.health_pool}   +{round(dragon_knight.effective_health_regen_rate, 2)}"
    mana_text = f"{round(dragon_knight.mana)} / {dragon_knight.mana_pool}   +{round(dragon_knight.mana_regeneration_rate, 2)}"
    health_text_surface = font.render(
        health_text,
        True,
        (255, 255, 255),
    )

    mana_text_surface = font.render(
        mana_text,
        True,
        (255, 255, 255),
    )

    display.blit(
        health_text_surface,
        (screen_width / 2 - len(health_text) * 3, screen_height / 2 + 10),
    )

    # total health bar
    pygame.draw.rect(
        display,
        (255, 255, 255),
        (screen_width / 2 - 50, screen_height / 2 - 5, 100, 10),
    )

    # actual health bar
    pygame.draw.rect(
        display,
        (0, 255, 0),
        (screen_width / 2 - 50, screen_height / 2 - 5, health_ratio, 10),
    )

    display.blit(
        mana_text_surface,
        (screen_width / 2 - len(mana_text) * 3, screen_height / 2 + 50 + 15),
    )
    # total mana bar
    pygame.draw.rect(
        display,
        (255, 255, 255),
        (screen_width / 2 - 50, screen_height / 2 + 50, 100, 10),
    )

    # actual mana bar
    pygame.draw.rect(
        display,
        (0, 0, 255),
        (screen_width / 2 - 50, screen_height / 2 + 50, mana_ratio, 10),
    )
    # render the dual buffer
    pygame.display.flip()

    # tick the fps clock by 30 fps
    fps_clock.tick(30)

    for debuff in debuffs:

        debuff.tick(clock=clock)
        if debuff.is_expired():
            debuffs.remove(debuff)

    for hero in heroes:
        hero.tick(clock=clock)

    # tick the game objects
    hero_animation.tick(clock=clock)
    ## (debuf - hero)
