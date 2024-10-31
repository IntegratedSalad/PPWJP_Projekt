import unittest
import logging
import sys
from pathlib import Path
from ..map import Hex, HexGrid

class HexGridBasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''
        Setup once per class, not once per every test method
        '''
        logging.basicConfig(
        filename="test_results.log",
        filemode="w",
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.DEBUG
        )

        cls.logger = logging.getLogger("HexGridBasicTest")
        cls.logger.setLevel(logging.DEBUG)
        cls.fh = logging.FileHandler('test_results.log')
        cls.fh.setLevel(logging.DEBUG)
        cls.fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
        cls.logger.addHandler(cls.fh)

    def setUp(self):
        self.radius = 0
        self.hexgrid = HexGrid(self.radius)

    def test_generating_grid(self):
        self.logger.info(f"Running test_generating_grid") # TODO: how to wrap this?
        middle_hex = Hex(3, 3)
        surface_height = 500
        radius = 10
        self.hexgrid.generate_grid(middle_hex, surface_height, radius)

        self.assertIsNotNone(self.hexgrid.grid)
        self.assertIsNotNone(self.hexgrid.tiles)

        self.logger.info(f"Offset Q: {self.hexgrid.offsetq}")
        self.logger.info(f"Offset R: {self.hexgrid.offsetr}")

        self.assertEqual(self.hexgrid.offsetq, 19)
        self.assertEqual(self.hexgrid.offsetr, 19)

    # TODO: Test that setting the grid and tiles, setting a hex in grid, at some coordinates,
    # allows for access of this particular hex in tiles list.

    # Make a few hexes and test accessing them by get_tile_from_hex, get_hex_at_x_y etc.
    # We don't need a surface to generate some hexes.
    # Just generate grid, mark some hexes, simulate mousepos_x, mousepos_y and use functions
    # flat_hex_to_pixel / pixel_to_flat_hex

if __name__ == "__main__":
    unittest.main()
