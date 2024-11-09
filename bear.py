# import pygame
from fsm import FSM, State
from enum import Enum

FEMALE_BEAR_CHANCE_ON_SPAWN = 20 # there will be less females than males

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

        self.brain = FSM()

    