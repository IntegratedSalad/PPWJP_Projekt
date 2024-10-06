import pygame
from pathlib import Path
from map import Map

COLOR_MOUNTAIN = (117, 99, 73)
COLOR_FOREST = (27, 117, 35)
COLOR_FIELD = (77, 212, 47)
COLOR_RIVER = (0, 90, 224)

'''
Pygame basics:
Surface is space onto which we can draw shapes; for example by calling
pygame.draw.rect when we have rect or multiple rects.
It can set color and copy these pixels onto passed surface.
Then, we can blit (copy) everything what we've composed
onto screen surface (main canvas) that gets drawn.
'''

'''
Class Slider
Composes of three rects:
on_rect = from 0 to button rect
off_rect = from button rect to self width
button_rect = separates on and off sides
'''
class Slider:
    def __init__(self, font, x, y, width, height, min_val, max_val, color_left=(31, 120, 255), color_right=(4, 51, 122), color_button=(255, 255, 255)) -> None:
        self.font = font
        self.x = x, # not needed (4, 51, 122)
        self.y = y, # not needed
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.color_left = color_left
        self.color_right = color_right
        self.color_button = color_button
        self.percent_on = 0
        self.current_value = 0

        self.update(self.percent_on)
        self.surface = self.get_composition()

    def get_composition(self) -> pygame.Surface:
        '''
        Blit this surface onto screen surface
        '''
        slider_surface = pygame.Surface((self.width, self.height))
        pygame.draw.rect(slider_surface, self.color_left, self.on_rect)
        pygame.draw.rect(slider_surface, self.color_right, self.off_rect)
        pygame.draw.rect(slider_surface, self.color_button, self.button_rect)
        return slider_surface
    
    def update(self, percent_on):
        self.percent_on = percent_on
        self.on_rect = pygame.Rect(0, 0, (self.percent_on / 100) * self.width, self.height)
        self.off_rect = pygame.Rect(self.on_rect.width, 0, self.width, self.height)
        self.button_rect = pygame.Rect(self.on_rect.width, 0, 0.16*self.width, self.height)
    
    def get_value(self):
        # Calculate value based on percent on
        pass
    
    '''
    mouse_x, mouse_y at the moment of click
    '''
    def slide(self, mouse_x, mouse_y) -> None:
        rel_x = abs(self.x - mouse_x)
        rel_y = abs(self.y - mouse_y)

        # new_percent_on =
        # self.update(new_percent_on)

'''
Class App
App sets everything up:
Surface to blit everything (screen)
Every instance that needs to be in memory for the whole time
Maybe App draws everything? At least for now.
'''
class App:
    WIDTH = 1024
    HEIGHT = 720

    def __init__(self) -> None:
        pygame.display.init()
        pygame.font.init()

        path_to_font_file = Path(".") / "pixelify_sans.ttf"
        self.main_font = pygame.font.Font(path_to_font_file, size=18)
        self.title_font = pygame.font.Font(path_to_font_file, size=30)
        self.screen = pygame.display.set_mode(size=(App.WIDTH, App.HEIGHT))
        self.map = None #Map(start_octaves=6, screen_width=App.WIDTH, screen_height=App.HEIGHT) 
        # TODO: it takes a huge amount of time to make map. First, blit to the screen that we're generating map
        # register font
        self.t_misioland = self.title_font.render("MisioLand", False, (255, 255, 255))

    def run(self):
        
        # Blit info about making a map
        # t_perlin_noise = self.main_font.render("Generating perlin noise...", False, (255, 255, 255))
        # Global surface, onto which GUI, map etc. are blit
        # self.screen.blit(t_perlin_noise, (App.WIDTH / 2, App.HEIGHT/ 2))
        # pygame.display.update()
        # self.map = Map(start_octaves=5.7, screen_width=App.WIDTH, screen_height=App.HEIGHT)

        mw, mh = self.draw_starting_screen()
        self.map = Map(start_octaves=5.7, map_width=mw, map_height=mh)
        self.draw_map_gen_screen()

    def draw_starting_screen(self) -> tuple[int, int]:
        
        # choose map dimensions, number of starting bears etc.
        slider1 = Slider(self.main_font, 0, 0, 50, 20, 0, 10)
        slider1.update(28)
        
        map_width = Map.MAP_WIDTH
        map_height = Map.MAP_HEIGHT

        rect_visualisation = pygame.Rect(0, 0, map_width, map_height)
        visualisation_surface = pygame.Surface((map_width, map_height))

        t_pressg = self.main_font.render("Press g to generate perlin noise...", False, (255, 255, 255))
        t_generating_noise = self.main_font.render("Generating noise...", False, (255, 255, 255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.screen.fill((0, 0, 0))
                        self.screen.blit(t_generating_noise, (App.WIDTH / 2 - len("Generating noise..."), App.HEIGHT / 2))
                        pygame.display.update()
                        return (350, 350)

            self.screen.blit(slider1.get_composition(), (80, 80))
            self.screen.blit(self.t_misioland, (App.WIDTH / 2 - len("misioland") - 60, 60))
            self.screen.blit(t_pressg, (App.WIDTH / 2 - len("Press g to generate perlin noise...") - 100, App.HEIGHT / 2 + 200))

            pygame.draw.rect(visualisation_surface, (171, 223, 255), rect_visualisation, 0, 5, 5, 5, 5, 5)
            self.screen.blit(visualisation_surface, (App.WIDTH / 2 - rect_visualisation.width/2, 100))

            pygame.display.update()
    
    def draw_map_gen_screen(self) -> None:
        # define clock
        # show generation of map 

        self.screen.fill((0, 0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            # Maybe put noise map onto different surface?
            # Yes, and then - scale that surface.
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
        pygame.font.quit()
        pygame.quit()
