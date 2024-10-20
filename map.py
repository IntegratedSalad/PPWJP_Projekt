from perlin_noise import PerlinNoise
from enum import Enum
from math import sqrt, sin, cos

MAX_FOOD = 50

CLOCK_DIR_12 = 2
CLOCK_DIR_1 = 1
CLOCK_DIR_4 = 0
CLOCK_DIR_6 = 5
CLOCK_DIR_7 = 4
CLOCK_DIR_10 = 3

class TileType(Enum):
    T_MOUNTAINS = 1
    T_FOREST = 2
    T_FIELD = 3
    T_DESERT = 4
    T_RIVER = 5

'''
Tile class
[...]
'''

class Tile:
    def __init__(self, hex, ttype) -> None:
        self.hex = hex # does Tile needs hex?
        self.ttype = ttype
        self.fmeat_quantity = 0
        self.fapple_quantity = 0
        self.water_quantity = 0
        self.pos_in_list = 0
        self.bears = []

'''
Point class

Simple structure representing x,y as Cartesian coordinates
'''

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

'''
HexGrid class

Starts with Hex at 0,0 which is the center of the grid.
Grid operates on axial coordinates.
Taken from https://www.redblobgames.com/grids/hexagons/

Hexagonal grid starts with leftmost hex with q=0, r=0
'''

class HexGrid:
    def __init__(self, size) -> None:
        self.size = size # no of rings
        self.grid = None
        self.directions = [Hex(1, 0), Hex(1, -1), Hex(0, -1), Hex(-1, 0), Hex(-1, 1), Hex(0, 1)]
        self.generate_grid()

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
        results = [center]
        for i in range(1, radius):
            results.extend(self.get_axial_ring(center, i))
        return results
    
    def generate_grid(self):
        # q - columns
        # r - rows
        self.grid = [[Tile(Hex(q, r), TileType.T_RIVER) for q in range(0, self.size)] for r in range(0, self.size)]

    @staticmethod
    def calculate_size_needed(width, height, hex_radius):
        '''
        Calculate N, where 2D array of hexes is NxN, needed
        to represent a hexagonal map from the generated perlin noise map.
        '''
        pass

    @staticmethod
    def cube_to_axial(cube: Cube):
        q = cube.q
        r = cube.r
        return Hex(q, r)
    
    @staticmethod
    def axial_to_cube(hex: Hex):
        q = hex.q
        r = hex.r
        s = -q-r
        return Cube(q, r, s)

    @staticmethod
    def flat_hex_to_pixel(radius, hex: Hex):
        x = radius * ((3.0/2)   * hex.q)
        y = radius * (sqrt(3)/2 * hex.q + sqrt(3) * hex.r)
        return (x, y)
    
    @staticmethod
    def pixel_to_flat_hex(point: Point, radius) -> int:
        q = ( 2.0/3 * point.x) / radius
        r = (-1.0/3 * point.x + sqrt(3)/3 * point.y) / radius

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

    def __init__(self, start_octaves, map_width, map_height) -> None:
        self.map_width = map_width
        self.map_height = map_height
        self.pnoise = PerlinNoise(octaves=start_octaves)
        self.noise_map = self.get_noise_map(self.map_width, self.map_height)
        self.hex_grid = HexGrid()

    def draw(self, screen) -> None:
        pass

    def get_noise_map_normalized(self, X, Y):
        oldMin = (-1.0)
        oldMax = 1.0
        newMax = 255.0
        newMin = 0.0
        oldRange = oldMax - oldMin
        newRange = newMax - newMin
        return [[((((self.pnoise([i/X, j/Y]) - oldMin) * newRange) / oldRange) + newMin) for j in range(X)] for i in range(Y)]
    
    def get_noise_map(self, X, Y):
        return [[self.pnoise([i/X, j/Y]) for j in range(X)] for i in range(Y)]

    def regenerate_noise(self, seed):
        pass