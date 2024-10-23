import pygame
from math import cos, pi, sin
from pathlib import Path
from map import Map, HexGrid, Point, Hex

COLOR_MOUNTAIN = (117, 99, 73)
COLOR_FOREST = (27, 117, 35)
COLOR_FIELD = (77, 212, 47)
COLOR_RIVER = (21, 67, 232)

DEFAULT_HEX_RADIUS = 14

'''
Pygame basics:
Surface is space onto which we can draw shapes; for example by calling
pygame.draw.rect when we have rect or multiple rects.
It can set color and copy these pixels onto passed surface.
Then, we can blit (copy) everything what we've composed
onto the screen surface (main canvas) that gets drawn.
'''

'''
Class Slider
Composes of three rects:
on_rect = from 0 to button rect
off_rect = from button rect to self width
button_rect = separates on and off sides
Maybe inherit from pygame.Rect?
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
        self.surface = None
        self.rect = None

        self.update(self.percent_on)
        button_width = 0.25 * self.width
        self.button_rect = pygame.Rect(self.on_rect.width, 0, button_width - button_width/2, self.height)
        self.surface = self.get_composition()

        self.value = self.min_val

    def get_composition(self) -> pygame.Surface:
        '''
        Returns surface to blit onto screen surface
        '''
        slider_surface = pygame.Surface((self.width, self.height))
        pygame.draw.rect(slider_surface, self.color_left, self.on_rect)
        pygame.draw.rect(slider_surface, self.color_right, self.off_rect)
        pygame.draw.rect(slider_surface, self.color_button, self.button_rect)
        self.rect = slider_surface.get_rect()

        return slider_surface
    
    def update(self, percent_on):
        self.percent_on = percent_on
        self.on_rect = pygame.Rect(0, 0, self.percent_on * self.width, self.height)
        self.off_rect = pygame.Rect(self.on_rect.width, 0, self.width, self.height)

    def set_value(self):
        # Calculate value based on percent on

        if self.percent_on <= 0:
            self.value = self.min_val
        elif self.percent_on >= 1:
            self.value = self.max_val
        else:
            self.value = round(self.min_val + ((self.max_val - self.min_val) * self.percent_on))

    '''
    mouse_x, mouse_y at the moment of click
    '''
    def slide(self, mouse_x, mouse_y) -> None:
        rel_x = abs(self.x - mouse_x)
        rel_y = abs(self.y - mouse_y)

        if rel_x < self.width - self.button_rect.width:
            self.button_rect.x = rel_x

        new_percent_on = (self.button_rect.x + self.button_rect.width / 2) / (self.width)
        new_percent_on = round(new_percent_on, 3)
        if (new_percent_on > 0.9):
            new_percent_on = 1
        if (new_percent_on < 0.1):
            new_percent_on = 0
        
        self.update(new_percent_on)
        self.set_value()

'''
Class App
App sets everything up:
Surface to blit everything (screen)
Every instance that needs to be in memory for the whole time
Maybe App draws everything? At least for now.
Maybe define class "View", that can have some return field
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
        self.little_font = pygame.font.Font(path_to_font_file, size=12)
        self.little_font_arial = pygame.font.SysFont("Arial", 10)
        self.screen = pygame.display.set_mode(size=(App.WIDTH, App.HEIGHT))
        self.map = None #Map(start_octaves=6, screen_width=App.WIDTH, screen_height=App.HEIGHT) 
        self.t_misioland = self.title_font.render("MisioLand", False, (255, 255, 255))

    def run(self):
        
        # Blit info about making a map
        # t_perlin_noise = self.main_font.render("Generating perlin noise...", False, (255, 255, 255))
        # Global surface, onto which GUI, map etc. are blit
        # self.screen.blit(t_perlin_noise, (App.WIDTH / 2, App.HEIGHT/ 2))
        # pygame.display.update()
        # self.map = Map(start_octaves=5.7, screen_width=App.WIDTH, screen_height=App.HEIGHT)

        mw, mh = self.draw_starting_screen()
        if mw is None or mh is None: return
        self.map = Map(start_octaves=5.7, map_width=mw, map_height=mh, hex_radius=DEFAULT_HEX_RADIUS)
        self.draw_map_gen_screen()

    def draw_starting_screen(self) -> tuple[int, int]:
        
        # choose map dimensions, number of starting bears etc.
        slider1 = Slider(self.main_font, 0, 0, 80, 20, 300, 450)
        # bear_slider = Slider
        # evolution_rate_slider = Slider
        
        map_width = Map.MAP_WIDTH
        map_height = Map.MAP_HEIGHT

        rect_visualisation = pygame.Rect(0, 0, map_width, map_height)
        visualisation_surface = pygame.Surface((Map.MAX_WIDTH, Map.MAX_HEIGHT))

        t_pressg = self.main_font.render("Press g to generate perlin noise...", False, (255, 255, 255))
        t_generating_noise = self.main_font.render("Generating noise...", False, (255, 255, 255))
        slider_rect = None # this is a slider rect that gets created after blitting

        hex_surf = pygame.Surface((100, 100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    return (None, None)
                
                if pygame.mouse.get_pressed()[0]:
                    mousepos = pygame.mouse.get_pos()
                    if slider_rect.collidepoint(mousepos):
                        slider1.slide(abs(mousepos[0]), mousepos[1])
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.screen.fill((0, 0, 0))
                        self.screen.blit(t_generating_noise, (App.WIDTH / 2 - len("Generating noise..."), App.HEIGHT / 2))
                        pygame.display.update()
                        return (slider1.value, slider1.value)

            self.screen.fill((0,0,0))
            visualisation_surface.fill((0,0,0))
            slider_rect = self.screen.blit(slider1.get_composition(), (App.WIDTH /2 - slider1.width / 2, App.HEIGHT/2 + 250))
            slider1.x, slider1.y = slider_rect.x, slider_rect.y
            slider1.rect.x, slider1.y = slider_rect.x, slider_rect.y
            self.screen.blit(self.t_misioland, (App.WIDTH / 2 - len("misioland") - 60, 30))
            self.screen.blit(t_pressg, (App.WIDTH / 2 - len("Press g to generate perlin noise...") - 100, App.HEIGHT / 2 + 300))

            rect_visualisation.width = slider1.value
            rect_visualisation.height = slider1.value
            t_map_size = self.main_font.render(f"Map size: {slider1.value}px", False, (255, 255, 255))
            self.screen.blit(t_map_size, (App.WIDTH / 2 - (len("Map size: px") + 3) - 50, App.HEIGHT / 2 + 220))
            pygame.draw.rect(visualisation_surface, (171, 223, 255), rect_visualisation, 0, 5, 5, 5, 5, 5)
            self.screen.blit(visualisation_surface, (App.WIDTH / 2 - rect_visualisation.width/2, 70))

            self.draw_polygon_on_surface(hex_surf, 20, (255, 255, 255), 6)
            self.screen.blit(hex_surf, (50, 50))

            pygame.display.update()
    
    def draw_map_gen_screen(self) -> None:
        # define clock
        # show generation of map

        # Mapa z szesciokatami takze musi byc na osobnym surface!!!
        self.screen.fill((0, 0, 0))

        map_surf = pygame.Surface((self.map.map_width, self.map.map_height))
        map_surf.fill((0, 0, 0))

        hex_grid_surf = pygame.Surface((self.map.map_width, self.map.map_height))
        hex_grid_surf.set_colorkey((0,0,0)) # make black transparent

        # hex_grid_surf.fill((0, 0, 0))

        # Slider do zmieniania hex_radius

        surface_center_point = Point.fromtuple(hex_grid_surf.get_rect().center)
        middle_hex = HexGrid.pixel_to_flat_hex(surface_center_point, self.map.hex_radius)
        # Make grid here
        self.map.hex_grid.generate_grid(middle_hex, hex_grid_surf.get_height(), self.map.hex_radius)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    return

            map_surf.fill((0,0,0))
            # Do we need to set_at continuously?
            for i, x in enumerate(self.map.noise_map):
                for j, nval in enumerate(x):
                    
                    if nval >= Map.T_MOUNTAIN_THRESH:
                        map_surf.set_at((j, i), COLOR_MOUNTAIN)

                    elif nval >= Map.T_FOREST_THRESH:
                        map_surf.set_at((j, i), COLOR_FOREST)
                        
                    elif nval >= Map.T_FIELD_THRESH:
                        map_surf.set_at((j, i), COLOR_FIELD)

                    else:
                        map_surf.set_at((j, i), COLOR_RIVER)
            
            # Blit map [V]
            # Blit hexes [V]
            # Make hexes selectable []
            # At the end, maybe make subset of hex map?
            # Those that are offscreen shouldn't be in memory

            self.draw_hex_map(hex_grid_surf, self.map.hex_radius)
            # or just scale the map_surf after blitting hex grid surf...
            map_surf.blit(hex_grid_surf, (0,0))
            # self.screen.blit(hex_grid_surf, (0,0))
            map_surf_scaled = pygame.transform.scale(map_surf, (self.map.map_width*1.5, self.map.map_height*1.5))
            self.screen.blit(map_surf_scaled, map_surf_scaled.get_rect(center=self.screen.get_rect().center))
            pygame.display.update()

    def draw_polygon_on_surface(self, surface: pygame.Surface, radius, color, vertex_count, width=1):
        n, r = vertex_count, radius
        pygame.draw.polygon(surface, color, [(surface.get_width()/2 + r * cos(2 * pi * i / n), surface.get_height()/2 + r * sin(2 * pi * i / n)) for i in range(n)], width=width)

    def draw_polygon_at_x_y(self, surface: pygame.Surface, x, y, radius, color, vertex_count, width=1):
        n, r = vertex_count, radius
        pygame.draw.polygon(surface, color, [(x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n)) for i in range(n)], width=width)

    def draw_hex_map(self, hex_map_surface: pygame.Surface, radius):
        '''
        Make a ring, starting from the middle of the map. 
        I think that this 2D array I am making
        is enough to support this. Just start drawing rings.
        Calculate the q,r coords of the middle hexagon and start from there:
        1. Get first hexagon at 0,0
        2. Get map rect and get middle x,y
        3. Convert x,y to hex.
        Calculate how many rings we need to support to fill the map.
        (MapHeight / 2) / Radius
        Q -> OFFSET TO THE LOWER RIGHT R -> ROW

        The idea would be to somehow blit these hexes once to map
        and never get this calculations in loop.
        Maybe make copy before clearing or something
        '''

        offsetq = self.map.hex_grid.offsetq
        offsetr = self.map.hex_grid.offsetr

        for r in range(0, self.map.hex_grid.size):
            for q in range(0, self.map.hex_grid.size):
                hex_to_draw = self.map.hex_grid.grid[q][r]
                if hex_to_draw is not None:
                    new_q = hex_to_draw.q - offsetq
                    new_r = hex_to_draw.r - offsetr
                    new_h = Hex(new_q, new_r)
                    point = HexGrid.flat_hex_to_pixel(radius, new_h)
                    x, y = point.x, point.y
                    t_hexpos = self.little_font_arial.render(f"Q:{new_q}R:{new_r},", False, (255, 255, 255))
                    hex_map_surface.blit(t_hexpos, (x-8,y-5))
                    self.draw_polygon_at_x_y(hex_map_surface, x, y, radius, (255,255,255), 6)

        # surface_center_point = Point.fromtuple(hex_map_surface.get_rect().center)
        # middle_hex = HexGrid.pixel_to_flat_hex(surface_center_point, radius)

        # n_rings = 14
        # for hex_vector in self.map.hex_grid.get_spiral_axial_ring(middle_hex, n_rings):
        #     # hex_vector is a offset vector from the middle

        #     print(f"DIFF:{self.map.hex_grid.axial_add(hex_vector, middle_hex)}")

        #     hex_to_draw = self.map.hex_grid.axial_add(hex_vector, Hex(0, 0))
        #     point = HexGrid.flat_hex_to_pixel(radius, hex_to_draw)
        #     x, y = point.x, point.y
        #     t_hexpos = self.little_font_arial.render(f"Q:{hex_to_draw.q}R:{hex_to_draw.r},", False, (255, 255, 255))
        #     hex_map_surface.blit(t_hexpos, (x-8,y-5))
        #     self.draw_polygon_at_x_y(hex_map_surface, x, y, radius, (255,255,255), 6)

    def quit(self) -> None:
        pygame.font.quit()
        pygame.quit()
