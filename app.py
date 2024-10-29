import pygame
from math import cos, pi, sin
from pathlib import Path
from map import Map, HexGrid, Point, Hex
from map import COLOR_RIVER, COLOR_MOUNTAIN, COLOR_FIELD, COLOR_FOREST, COLOR_SELECT_GREEN
DEFAULT_HEX_RADIUS = 8
MIN_HEX_RADIUS = 5
MAX_HEX_RADIUS = 18

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

Screens:

1. Mapgen
2. Hexgen
3. Beargen & biomegen
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
        self.t_misioland = self.title_font.render("MisioLand", True, (255, 255, 255))

    def run(self):
        # TODO: Maybe FSM for screen choice?
        mw, mh = self.draw_mapgen_screen()
        if mw is None or mh is None: return
        self.map = Map(start_octaves=5.7, map_width=mw, map_height=mh, hex_radius=DEFAULT_HEX_RADIUS)
        self.draw_hexgen_screen()

    def draw_mapgen_screen(self) -> tuple[int, int]:
        
        # choose map dimensions, number of starting bears etc.
        slider1 = Slider(self.main_font, 0, 0, 80, 20, 300, 450)
        # bear_slider = Slider
        # evolution_rate_slider = Slider
        
        map_width = Map.MAP_WIDTH
        map_height = Map.MAP_HEIGHT

        rect_visualisation = pygame.Rect(0, 0, map_width, map_height)
        visualisation_surface = pygame.Surface((Map.MAX_WIDTH, Map.MAX_HEIGHT))

        t_pressg = self.main_font.render("Press g to generate perlin noise...", True, (255, 255, 255))
        t_generating_noise = self.main_font.render("Generating noise...", True, (255, 255, 255))
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
            self.screen.blit(t_pressg, (App.WIDTH / 2 - len("Press g to generate perlin noise and hexgrid...") - 100, App.HEIGHT / 2 + 300))

            rect_visualisation.width = slider1.value
            rect_visualisation.height = slider1.value
            t_map_size = self.main_font.render(f"Map size: {slider1.value}px", False, (255, 255, 255))
            self.screen.blit(t_map_size, (App.WIDTH / 2 - (len("Map size: px") + 3) - 50, App.HEIGHT / 2 + 220))
            pygame.draw.rect(visualisation_surface, (171, 223, 255), rect_visualisation, 0, 5, 5, 5, 5, 5)
            self.screen.blit(visualisation_surface, (App.WIDTH / 2 - rect_visualisation.width/2, 70))

            self.draw_polygon_on_surface(hex_surf, 20, (255, 255, 255), 6)
            self.screen.blit(hex_surf, (50, 50))

            pygame.display.update()
    
    def draw_hexgen_screen(self) -> pygame.Surface:
        '''
        This method should return hexagon map,
        with each hexagon in one solid color representing each biome.
        '''
        # define clock
        # show generation of map

        # Mapa z szesciokatami takze musi byc na osobnym surface!!!
        self.screen.fill((0, 0, 0))

        world_surf = pygame.Surface((self.map.map_width, self.map.map_height))
        world_surf.fill((0, 0, 0))
        world_surf_scaled = None

        hex_grid_surf = pygame.Surface((self.map.map_width, self.map.map_height))
        hex_grid_surf.set_colorkey((0,0,0)) # make black transparent
        # Slider do zmieniania hex_radius

        surface_center_point = Point.fromtuple(hex_grid_surf.get_rect().center)
        middle_hex = HexGrid.pixel_to_flat_hex(surface_center_point, self.map.hex_radius)
        t_generating_hexgrid = self.main_font.render("Generating hexgrid...", True, (255,255,255))
        self.screen.fill((0,0,0))
        self.screen.blit(t_generating_hexgrid, (App.WIDTH / 2 - len("Generating hexgrid..."), App.HEIGHT / 2))
        pygame.display.update()
        self.map.hex_grid.generate_grid(middle_hex, hex_grid_surf.get_height(), self.map.hex_radius)

        select_hex_surface = pygame.Surface((self.map.map_width, self.map.map_height))
        select_hex_surface.fill((0, 0, 0))
        select_hex_surface.set_colorkey((0,0,0))
        # TODDO: We can also separate the filled hexes and completely discard the noise

        '''
        Set pixels here, because in self.draw_hex_map
        we will be iterating over pixels in each hexagon,
        to determine the 'biome'
        '''
        for i, x in enumerate(self.map.noise_map):
            for j, nval in enumerate(x):
                if nval >= Map.T_MOUNTAIN_THRESH:
                    world_surf.set_at((j, i), COLOR_MOUNTAIN)
                elif nval >= Map.T_FOREST_THRESH:
                    world_surf.set_at((j, i), COLOR_FOREST)
                elif nval >= Map.T_FIELD_THRESH:
                    world_surf.set_at((j, i), COLOR_FIELD)
                else:
                    world_surf.set_at((j, i), COLOR_RIVER)
        world_surf_scaled = pygame.transform.scale(world_surf, (self.map.map_width*1.5, self.map.map_height*1.5))

        hex_grid_surf.blit(world_surf_scaled, (0, 0)) # blit perlin noise onto hex surface, to analyze the data
        self.set_hex_map(hex_grid_surf, self.map.hex_radius) # blit hexes onto surface once

        t_keypress = self.main_font.render("(G)", False, (255,255,255))
        t_next = self.main_font.render("Next ->", False, (255,255,255))

        select_hex_surface_scaled = None
        while True:
            select_hex_surface.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.screen.fill((0, 0, 0))
                        pygame.display.update()
                        return world_surf_scaled
            
            mousepos_x, mousepos_y = pygame.mouse.get_pos()
            if world_surf_scaled is not None:
                world_surf_scaled = pygame.transform.scale(world_surf_scaled, (self.map.map_width*1.5, self.map.map_height*1.5)).get_rect(center=self.screen.get_rect().center) # scale it in case it wasn't
                _x, _y = world_surf_scaled.x, world_surf_scaled.y
                if world_surf_scaled.collidepoint(mousepos_x, mousepos_y):
                    mousepos_x -= _x
                    mousepos_y -= _y
                    mousepos_x /= 1.5
                    mousepos_y /= 1.5
                    print(mousepos_x, mousepos_y)

                    hex = HexGrid.pixel_to_flat_hex(Point.fromtuple((mousepos_x, mousepos_y)), self.map.hex_grid.radius)
                    if hex is not None:
                        print(hex)
                        hex_to_draw = self.map.hex_grid.get_offset_hex(hex)
                        point = HexGrid.flat_hex_to_pixel(self.map.hex_grid.radius, hex)
                        px, py = point.x, point.y
                        self.draw_polygon_at_x_y(select_hex_surface, px, py, self.map.hex_grid.radius, COLOR_SELECT_GREEN, 6, width=0)

                # TODO: If grid resized and r pressed, blit again
            # At the end, maybe make subset of hex map?
            # Those that are offscreen shouldn't be in memory

            world_surf.blit(hex_grid_surf, (0,0))
            world_surf_scaled = pygame.transform.scale(world_surf, (self.map.map_width*1.5, self.map.map_height*1.5))
            self.screen.blit(world_surf_scaled, world_surf_scaled.get_rect(center=self.screen.get_rect().center))
            self.screen.blit(t_keypress, (App.WIDTH - len("(G)")- 90, self.screen.get_rect().centery))
            self.screen.blit(t_next, (App.WIDTH - len("Next ->") - 100, self.screen.get_rect().centery + 11))
            select_hex_surface_scaled = pygame.transform.scale(select_hex_surface, (self.map.map_width*1.5, self.map.map_height*1.5))
            self.screen.blit(select_hex_surface_scaled, (world_surf_scaled.get_rect(center=self.screen.get_rect().center)))
            pygame.display.update()

    def draw_biomegen_screen():
        pass

    def draw_polygon_on_surface(self, surface: pygame.Surface, radius, color, vertex_count, width=1):
        n, r = vertex_count, radius
        pygame.draw.polygon(surface, color, [(surface.get_width()/2 + r * cos(2 * pi * i / n), surface.get_height()/2 + r * sin(2 * pi * i / n)) for i in range(n)], width=width)

    def draw_polygon_at_x_y(self, surface: pygame.Surface, x, y, radius, color, vertex_count, width=1) -> pygame.Rect:
        n, r = vertex_count, radius
        return pygame.draw.polygon(surface, color, [(x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n)) for i in range(n)], width=width)

    def count_pixels_in_polygon(self, polygon: pygame.Rect):
        pass

    def set_hex_map(self, hex_map_surface: pygame.Surface, radius):
        '''
        Make a ring, starting from the middle of the map. 
        Hex grid' grid should be initialized by now.
        This function draws hexagons in order to retrieve Rects
        and analyze pixels within these rects to determine the tile
        type of the hexagon.
        '''

        for r in range(0, self.map.hex_grid.size):
            for q in range(0, self.map.hex_grid.size):
                hex_to_draw = self.map.hex_grid.grid[q][r]
                if hex_to_draw is not None:
                    new_h = self.map.hex_grid.get_offset_hex(hex_to_draw)
                    point = HexGrid.flat_hex_to_pixel(radius, new_h)
                    px, py = point.x, point.y
                    hex_rect = self.draw_polygon_at_x_y(hex_map_surface, px, py, radius, (255,255,255), 6) # outline

                    hw, hh = hex_rect.size
                    hx, hy = hex_rect.x, hex_rect.y
                    color_count = {COLOR_MOUNTAIN: 0,
                                   COLOR_FOREST: 0,
                                   COLOR_FIELD: 0,
                                   COLOR_RIVER: 0}
                    
                    for x in range(hx, hx+hw):
                        for y in range(hy, hy+hh):
                            color = tuple(hex_map_surface.get_at((y,x)))
                            if color in color_count.keys():
                                color_count[color] += 1

                    max_color = max(color_count, key=color_count.get)

                    tile_type = self.map.hex_grid.get_tile_type_from_color(pygame.Color(max_color))
                    self.map.hex_grid.tiles[q][r].ttype = tile_type

                    self.draw_polygon_at_x_y(hex_map_surface, px, py, radius-1, max_color, 6, width=0)

    def draw_hex_map(self, hex_map_surface: pygame.Surface, radius):
        pass
        
    def quit(self) -> None:
        pygame.font.quit()
        pygame.quit()
