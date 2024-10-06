import pygame
from perlin_noise import PerlinNoise
from enum import Enum

MAX_FOOD = 50

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
    def __init__(self, ttype) -> None:
        self.ttype = ttype
        self.fmeat_quantity = 0
        self.fapple_quantity = 0
        self.water_quantity = 0

'''
Map class
Default noise will be set at the time of creation of the Map.
The user can generate a Map before starting simulation by providing a seed.
This seed will be taken to create the map, however, upon running the program,
default map (generated) will be used.
Map has a 2D array (tiles) which corresponds to the hexes.

Noise is drawn, by seeing, if the value exceeds a certain threshold.

Hexes are generated from what values dominate in the hex area
'''

class Map:

    MAP_WIDTH = 500
    MAP_HEIGHT = 500

    T_MOUNTAIN_THRESH = 0.4
    T_FOREST_THRESH = 0.09
    T_FIELD_THRESH = 0.02
    T_RIVER_THRESH = -0.1

    def __init__(self, start_octaves, screen_width, screen_height) -> None:
        self.pnoise = PerlinNoise(octaves=start_octaves)
        self.noise_map = self.get_noise_map(Map.MAP_WIDTH, Map.MAP_HEIGHT)
        self.tiles = None

    def generate_tiles(self) -> None:
        if self.noise is None:
            return

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