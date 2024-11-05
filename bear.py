# import pygame
from fsm import FSM, State
from enum import Enum

class MetabolismType(Enum):
    SLOW = 1
    NORMAL = 2
    FAST = 3

class StateLookForFood(State):
    def __init__(self, type):
        super().__init__(type)
    
    def __call__(self, *args, **kwargs):
        return

class Bear:
    def __init__(self,
                 sex,
                 energy=0,
                 hunger=0,
                 power=0,
                 reproductivity=0,
                 repr_ability=0,
                 age=0,
                 metabolism=MetabolismType.NORMAL
                 ):
        self.energy = energy
        self.sex = sex
        self.hunger = hunger
        self.power = power
        self.reproductivity = reproductivity
        self.repr_ability = repr_ability
        self.age = age
        self.metabolism = metabolism

        self.brain = FSM()

    