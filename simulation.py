from bear import Bear
import pygame

class Simulation:
    '''
    Simulation class defining logic for simulation
    World surface shall not ever be modified by this class.
    Simulation should recieve a copy of the hexgrid and modify its contents
    like tiles and information.
    Maybe don't modify but return what to modify to the App?

    TODO: Should this class draw anything?
    '''
    def __init__(self, world_surface: pygame.Surface):
        self.bear_surface = pygame.Surface(world_surface.get_size()) # should this class create that?

    def get_next_tick(self):
        '''
        Maybe this method returns things to update?
        Returns tiles etc?
        '''
        pass

    def run(self):
        pass
