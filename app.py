import pygame
from map import Map

'''
App sets everything up:
Surface to blit everything (screen)
Every instance that needs to be in memory for the whole time
Maybe App draws everything? At least for now
'''

COLOR_MOUNTAIN = (117, 99, 73)
COLOR_FOREST = (27, 117, 35)
COLOR_FIELD = (77, 212, 47)
COLOR_RIVER = (0, 90, 224)

class App:
    WIDTH = 1024
    HEIGHT = 720

    def __init__(self) -> None:
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=(App.WIDTH, App.HEIGHT))
        self.map = None #Map(start_octaves=6, screen_width=App.WIDTH, screen_height=App.HEIGHT) 
        # TODO: it takes a huge amount of time to make map. First, blit to the screen that we're generating map
        # register font
        
    def run(self):
        
        # Blit info about 

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            for i, x in enumerate(self.map.noise_map):
                for j, nval in enumerate(x):
                    
                    if nval >= Map.T_MOUNTAIN_THRESH:
                        self.screen.set_at((j, i), COLOR_MOUNTAIN)
                    
                    elif nval >= Map.T_FOREST_THRESH:
                        self.screen.set_at((j, i), COLOR_FOREST)

                    elif nval >= Map.T_FIELD_THRESH:
                        self.screen.set_at((j, i), COLOR_FIELD)
                    
                    else:
                        self.screen.set_at((j, i), COLOR_RIVER)
            
            pygame.display.update()

    def quit(self) -> None:
        pygame.quit()