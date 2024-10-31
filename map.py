from perlin_noise import PerlinNoise
from pygame import Color
from enum import Enum
from math import sqrt

MAX_FOOD = 50

CLOCK_DIR_12 = 2
CLOCK_DIR_1 = 1
CLOCK_DIR_4 = 0
CLOCK_DIR_6 = 5
CLOCK_DIR_7 = 4
CLOCK_DIR_10 = 3

COLOR_MOUNTAIN = (117, 99, 73, 255)
COLOR_FOREST = (27, 117, 35, 255)
COLOR_FIELD = (77, 212, 47, 255)
COLOR_RIVER = (21, 67, 232, 255)
COLOR_SELECT_GREEN = (0, 255, 0, 255)

class TileType(Enum):
    T_MOUNTAINS = 1
    T_FOREST = 2
    T_FIELD = 3
    T_DESERT = 4
    T_RIVER = 5
    T_VOID = 6

color_to_type_map = {COLOR_MOUNTAIN : TileType.T_MOUNTAINS, 
                     COLOR_FOREST : TileType.T_FOREST,
                     COLOR_FIELD : TileType.T_FIELD,
                     COLOR_RIVER: TileType.T_RIVER}

tile_type_to_str = {TileType.T_MOUNTAINS: "mountains",
                    TileType.T_FOREST: "forest",
                    TileType.T_FIELD: "field",
                    TileType.T_DESERT: "desert",
                    TileType.T_RIVER: "river",
                    TileType.T_VOID: "void"}

'''
Tile class
[...]
'''

class Tile:
    def __init__(self, ttype) -> None:
        self.ttype = ttype # biome
        self.fmeat_quantity = 0
        self.fapple_quantity = 0
        self.water_quantity = 0
        self.pos_in_list = 0
        self.bears = []

    def __str__(self):
        return f"TYPE: {self.ttype}"
    
    def get_tile_type_str(self):
        return tile_type_to_str[self.ttype]

'''
Point class

Simple structure representing x,y as Cartesian coordinates
'''

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"X: {self.x} Y:{self.y}"
    
    @staticmethod
    def fromtuple(tuple):
        return Point(tuple[0], tuple[1])

'''
Cube class
'''

class Cube:
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s

'''
Hex class

Class represents axial coordinates of one hexagonal polygon
This class is independent of the actual graphical representation
'''

class Hex:
    def __init__(self, q, r) -> None:
        self.q = q
        self.r = r

    def __str__(self):
        return f"Q:{self.q} R: {self.r}"
    
'''
HexGrid class

Starts with Hex at 0,0 which is the center of the grid.
Grid operates on axial coordinates.
Taken from https://www.redblobgames.com/grids/hexagons/

Hexagonal grid starts with leftmost hex with q=0, r=0
Hexagonal grid is composed of flat-top oriented hexagons.

TODO: Draw pointy-top hexagons or try to make a ring, starting from
      the middle of the map. I think that this 2D array I am making
      is enough to support this. Just start drawing rings.
      Calculate the q,r coords of the middle hexagon and start from there:
      1. Get first hexagon at 0,0
      2. Get map rect and get middle x,y
      3. Convert x,y to hex.
      Calculate how many rings we need to support to fill the map.
      (MapHeight / 2) / Radius 
'''

class HexGrid:
    def __init__(self, radius, size=None) -> None:
        self.size = size # no of rings
        # print(f"Hex grid size: {self.size}")

        '''
        grid and tiles are corelated.
        accessing them by q,r accesses an individual Hex with its type
        '''
        self.grid = None
        self.tiles = None
        self.directions = [Hex(1, 0), Hex(1, -1), Hex(0, -1), Hex(-1, 0), Hex(-1, 1), Hex(0, 1)]
        self.radius = radius
        self.maxr = 0
        self.maxq = 0
        self.offsetq = 0
        self.offsetr = 0

    def axial_direction(self, dir):
        return self.directions[dir]

    def axial_add(self, hex: Hex, vec: Hex):
        '''
        Return a Hex, by providing an offset vector from it.
        When searching for a hex, use this object returned here
        as a struct for storing q and r params in a grid,
        with indices q,r.
        '''
        return Hex(hex.q + vec.q, hex.r + vec.r)

    def axial_neighbor(self, hex: Hex, dir):
        return self.axial_add(hex, self.axial_direction(dir))
    
    def axial_scale(self, hex: Hex, factor):
        return Hex(hex.q * factor, hex.r * factor)
    
    def get_axial_ring(self, center_hex: Hex, radius):
        results = []
        next_hex = self.axial_add(center_hex, self.axial_scale(self.axial_direction(4), radius))
        for i in range(0, 6):
            for _ in range(0, radius):
                results.append(next_hex)
                next_hex = self.axial_neighbor(next_hex, i)
        return results
    
    def get_spiral_axial_ring(self, center: Hex, radius):
        '''
        Radius means N number of rings
        '''
        results = [center]
        for i in range(1, radius):
            results.extend(self.get_axial_ring(center, i))
        return results
    
    def generate_grid(self, middle_hex, surface_height, radius):
        """
        Generate grid

        Generating grid involves setting the self.grid and self.tiles
        attributes of this class.

        Set self.size to the rough estimate of surface height divided by hex radius

        All of the tile types in self.tiles are set to T_VOID.
        All of the hexes in self.grid are set to None, and then,
        certain number of them are set according to the spiral pattern.

        We calculate n_rings, which is the number of ring shapes around the
        middle_hex - essentialy the q,r coordinates of a hexagon
        placed in the middle of the map surface.
        N rings equals height divided by 2 divided by hex radius
        This N rings are then generated with get_spiral_axial_ring.
        All of the hexagons' coordinates are then shifted by a global offset.
        We want these hexagons (their coordinates q,r) to function as list indeces,
        and negative values are not suited for this.

        After this, all hexes of the spiral pattern are set into the correct
        places at q,r in the 2D list self.grid.
        """
        # q - columns
        # r - rows

        n_rings = HexGrid.calculate_axial_rings_needed(surface_height, radius)
        self.size = surface_height // radius
        # print(f"Size: {self.size}")
        # print(f"Rings: {n_rings}")
        # print(f"S Height: {surface_height}")
        self.grid = [[None for r in range(0, self.size)] for q in range(0, self.size)]
        self.tiles = [[Tile(TileType.T_VOID) for r in range(0, self.size)] 
                      for q in range(0, self.size)]

        minq = 1000
        minr = 1000
        hexes = []

        for next_hex in self.get_spiral_axial_ring(middle_hex, n_rings):
            hex_to_draw = self.axial_add(next_hex, Hex(0, 0)) # offset from start
            if hex_to_draw.q < minq:
                minq = hex_to_draw.q
            if hex_to_draw.r < minr:
                minr = hex_to_draw.r

            if hex_to_draw.q > self.maxq:
                self.maxq = hex_to_draw.q
            if hex_to_draw.r > self.maxr:
                self.maxr = hex_to_draw.r
            hexes.append(hex_to_draw)

        self.offsetq = -minq
        self.offsetr = -minr
        for hex in hexes:
            hex.q += self.offsetq
            hex.r += self.offsetr
            self.grid[hex.q][hex.r] = hex

    # @staticmethod
    # def calculate_grid_size_needed(width, height, hex_radius):
    #     '''
    #     Calculate N, where 2D array of hexes is NxN, needed
    #     to represent a hexagonal map from the generated perlin noise map.

    #     '''
    #     return (width//hex_radius, height//hex_radius)

    def get_tile_type_from_color(self, color: Color) -> TileType:
        return color_to_type_map[tuple(color)]

    def get_hex_at_x_y(self, x, y):
        hex = HexGrid.pixel_to_flat_hex(Point(x, y), self.radius)
        return self.grid[hex.q][hex.r]

    def get_tile_at_x_y(self, x, y):
        hex = HexGrid.pixel_to_flat_hex(Point(x, y), self.radius)
        return self.tiles[hex.q][hex.r]
    
    def get_tile_from_hex(self, hex) -> Tile:
        return self.tiles[hex.q][hex.r]

    def get_offset_hex(self, hex):
        new_q = hex.q - self.offsetq
        new_r = hex.r - self.offsetr
        return Hex(new_q, new_r)
    
    def get_deoffset_hex(self, hex):
        new_q = hex.q + self.offsetq
        new_r = hex.r + self.offsetr
        return Hex(new_q, new_r)

    @staticmethod
    def calculate_axial_rings_needed(height, hex_radius):
        return ((height // 2) // (hex_radius) - 2)

    @staticmethod
    def cube_to_axial(cube: Cube) -> Hex:
        q = cube.q
        r = cube.r
        return Hex(q, r)

    @staticmethod
    def axial_to_cube(hex: Hex) -> Cube:
        q = hex.q
        r = hex.r
        s = -q-r
        return Cube(q, r, s)

    @staticmethod
    def flat_hex_to_pixel(radius, hex: Hex) -> Point:
        x = radius * ((3.0/2)   * hex.q)
        y = radius * ((sqrt(3)/2) * hex.q + sqrt(3.0) * hex.r)
        return Point(x, y)
    
    @staticmethod
    def pixel_to_flat_hex(point: Point, radius) -> Hex:
        q = ( 2.0/3 * point.x) / radius
        r = (-1.0/3 * point.x + sqrt(3)/3 * point.y) / radius
        return HexGrid.axial_round(Hex(q, r))

    @staticmethod
    def cube_round(cube: Cube):
        q = round(cube.q)
        r = round(cube.r)
        s = round(cube.s)

        q_diff = abs(q - cube.q)
        r_diff = abs(r - cube.r)
        s_diff = abs(s - cube.s)

        if q_diff > r_diff and q_diff > s_diff:
            q = -r-s
        elif r_diff > s_diff:
            r = -q-s
        else:
            s = -q-r

        return Cube(q, r, s)
    
    @staticmethod
    def axial_round(hex: Hex):
        return HexGrid.cube_to_axial(HexGrid.cube_round(HexGrid.axial_to_cube(hex)))

'''
Map class
Default noise will be set at the time of creation of the Map.
The user can generate a Map before starting simulation by providing a seed and size.
Map has a 2D array (tiles) which corresponds to the hexes.
Noise is drawn, by checking if the value exceeds a certain threshold.
Hexes are generated from what values dominate in the hex area

TODO: This class should provide an interface for drawing, utilizing the
methods in HexGrid.
'''

class Map:

    MAP_WIDTH = 350
    MAP_HEIGHT = 350

    MAX_WIDTH = 500
    MAX_HEIGHT = 500

    T_MOUNTAIN_THRESH = 0.31
    T_FOREST_THRESH = 0.13
    T_FIELD_THRESH = 0.04
    T_RIVER_THRESH = -0.03

    def __init__(self, start_octaves, map_width, map_height, hex_radius) -> None:
        self.map_width = map_width
        self.map_height = map_height
        self.hex_radius = hex_radius
        self.pnoise = PerlinNoise(octaves=start_octaves)
        self.noise_map = self.get_noise_map(self.map_width, self.map_height)
        # assuming width and height are the same
        self.hex_grid = HexGrid(self.hex_radius)

    def get_noise_map_normalized(self, X, Y):
        oldMin = (-1.0)
        oldMax = 1.0
        newMax = 255.0
        newMin = 0.0
        oldRange = oldMax - oldMin
        newRange = newMax - newMin
        return [[((((self.pnoise([i/X, j/Y]) - oldMin) * newRange) / oldRange) + newMin) 
                 for j in range(X)] for i in range(Y)]
    
    def get_noise_map(self, X, Y):
        return [[self.pnoise([i/X, j/Y]) for j in range(X)] for i in range(Y)]

    def initialize_grid(self):
        """
        Maybe this function as an interface for this hexgrid?
        """
        pass