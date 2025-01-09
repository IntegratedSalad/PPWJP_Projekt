from fsm import FSM, State
from enum import Enum
from pygame.sprite import Sprite
from pygame import Surface, Rect
# from map import Point

FEMALE_BEAR_CHANCE_ON_SPAWN = 20 # % there will be less females than males
BEAR_CHANCE_SPAWN_ON_TILE = 65 # %

class MetabolismType(Enum):
    SLOW = 1
    NORMAL = 2
    FAST = 3

class SexType(Enum):
    FEMALE = 0
    MALE = 1

class BearType(Enum):
    BROWN = 0
    VEGETARIAN = 1
    CARNIVOROUS = 3
    PACIFIST = 4
    SOCIAL = 5
    LONER = 6

'''
Define states:
What each state should get?
'''

class StateLookForFood(State):
    def __init__(self, type):
        super().__init__(type)
    
    def __call__(self, *args, **kwargs):
        return

'''
Class BearSprite
'''
class BearSprite(Sprite):

    def __init__(self,
                 q,
                 r,
                 body_color,
                 eye_color,
                 width, # usually radius
                 height,
                 hex_to_pixel_func):
       Sprite.__init__(self)
       self.q = q
       self.r = r
       self.width = width
       self.height = height
       self.body_color = body_color
       self.eye_color = eye_color
       self.image = Surface((width, height))
       self.rect = self.image.get_rect()
    #    self.set_image(self.image)
       self.hex_to_pixel_func = hex_to_pixel_func # returns Point
       self.update_position()

    def update_position(self):
        x, y = self.hex_to_pixel_func(self.width, self.q, self.r)
        print(f"sprite x,y: {x},{y}")
        self.rect.topleft = (x,y)

    def update(self, *args, **kwargs):
        # TODO: Pass q,r to determine position
        self.update_position()

    def draw_bear_on_surface(self, surf: Surface) -> Rect:
        '''
        It's better to use Group class
        is this surface the global surface (for all bears)
        or is this a surface for individual bear?

        Maybe use a local surface, and then blit this surface continuously
        over the map.
        '''
        return surf.blit(self.image)

    def set_image(self, img: Surface) -> None:
        self.image = img
        self.rect = self.image.get_rect(center=self.rect.center)

    def __str__(self):
        return f"q: {self.q} r: {self.r} image: w:{self.image.get_width()} h: {self.image.get_height()}\
                 rect w:{self.rect.w} h: {self.rect.h}"

class Bear:
    '''
    Base class for bear.
    Plain, brown bear
    '''
    def __init__(self,
                 sex,
                 btype=BearType.BROWN,
                 energy=0,
                 hunger=0,
                 power=0,
                 reproductivity=0,
                 repr_ability=0,
                 age=0,
                 metabolism=MetabolismType.NORMAL
                 ):
        self.energy = energy
        self.btype = btype
        self.sex = sex
        self.hunger = hunger
        self.power = power
        self.reproductivity = reproductivity
        self.repr_ability = repr_ability
        self.age = age
        self.metabolism = metabolism

        # sprite?
        self.sprite = None

        # Each of the Bears has to have a q,r coordinates
        # All the drawing etc. is managed by the BearSprite

        # Problem jest taki - Mamy liste w map.hex_grid.tiles[q][r].bears
        # Jak rozdzielic logike chodzenia misiów (ich interakcji) od rysowania?

        self.brain = FSM()

    def set_sprite(self, sprite: Sprite):
        self.sprite = sprite
