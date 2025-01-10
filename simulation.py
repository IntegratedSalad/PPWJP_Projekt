from bear import Bear
import pygame
from map import TileType
from publisher import Publisher
import random

class Simulation(Publisher):
    '''
    Simulation class defining logic for simulation
    World surface shall not ever be modified by this class.
    Simulation should recieve a copy of the hexgrid and modify its contents
    like tiles and information.
    Maybe don't modify but return what to modify to the App?

    Should this class draw anything? No.

    First: Implement Publish/Subscriber architecture -> Simulation is the publisher
    
    How this works:
    We iterate through tiles looking for bears.
    If there is a bear, its brain (FSM) acts upon the state in which he currently is.

    '''
    def __init__(self):
        super().__init__()
        self.hex_grid = None

    def set_hex_grid(self, hg):
        self.hex_grid = hg

    def simulate_next_turn(self):
        '''
        Maybe this method returns things to update?
        Returns tiles etc?
        '''
        # print("Simulating turn...")
        self.simulate_bear_action()

    def simulate_bear_action(self):

        # TODO: For now, simulate their random movement

        for r in range(self.hex_grid.size):
            for q in range(self.hex_grid.size):
                if self.hex_grid.tiles[q][r] is not None:
                    tile = self.hex_grid.tiles[q][r]
                    tiletype = tile.ttype
                    if tiletype != TileType.T_VOID and tiletype != TileType.T_RIVER:
                        if len(tile.bears) > 0:
                            bear = tile.bears[0]
                            if bear is not None:
                                # For now, move manually in random dir
                                rdq = random.randint(-1, 1)
                                rdr = random.randint(-1, 1)
                                # This way, App will call map, hex_grid and handle any logic with drawing the bears
                                self.publish("bear_moved", {'bear': bear, 'orig_q': q, 'orig_r': r, 'dq': rdq, 'dr': rdr})

    def simulate_plant_growth(self):
        pass

    def run(self, hex_grid):
        print("Running simulation...")
        
        self.set_hex_grid(hex_grid)
        self.simulate_next_turn()
