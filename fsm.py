from abc import abstractmethod, ABCMeta
from enum import Enum

class StateType(Enum):
    STATE_LOOKING_FOR_FOOD = 1
    STATE_LOOKING_FOR_MATE = 2
    STATE_EATING = 3
    STATE_FLEEING = 4
    STATE_WAITING = 5
    STATE_HUNT = 6
    STATE_STARVING = 7
    STATE_SLEEPING = 8
    STATE_DEAD = 9

class State(ABCMeta):
    '''
    State is a callable with a type.
    '''
    def __init__(self, type: StateType):
        self.name = type

    @abstractmethod
    def __call__(self, *args, **kwargs) -> dict:
        pass

class FSM:
    '''
    Finite State Machine
    FSM facilitate a mechanism for changing states.
    '''
    def __init__(self, beginning_state: State=None):
        self.active_state = beginning_state
        self.transitions = []

    def update(self, *args, **kwargs):
        if self.active_state is not None:
            self.active_state(*args, **kwargs)
    
    def set_state(self, state: State):
        self.active_state = state

    def define_transition(self, state_primary: State, state_secondary: State):
        '''
        states are functions
        '''
        transition = (state_primary, state_secondary)
        if transition not in self.transitions:
            self.transitions.append(transition)

    def transition(self, state_to: State, *args, **kwargs) -> None:
        '''
        If this idea becomes too slow, transitioning will have to be implemented
        outside
        '''
        for possibility in self.transitions:
            if (possibility[0] == self.active_state and
                possibility[1] == state_to):
                self.set_state(state_to)
                self.update(*args, **kwargs)
                return
        
        
