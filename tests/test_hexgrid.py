import unittest
import logging
from ..map import Hex, HexGrid
# from functools import wraps

class HexGridBasicTest(unittest.TestCase):
    
    # def print_header(self): # outer decorator, assignment of test_func = print_header() returns dec
    #     def dec(f): # function that is assigned to test_func and invoked, when test is invoked 
    #         @wraps(f) # preserve information about f, our test_func
    #         def wrapper(*args, **kwargs):
    #             self.logger.info(f"Running {f.__name__}")
    #             r = f(*args, **kwargs)
    #             return r
    #         return wrapper
    #     return dec

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

    # TODO: Test setting the grid and tiles, setting a hex in grid, at some coordinates,
    # allows for access of this particular hex in tiles list.

    # TODO: Make a few hexes and test accessing them by get_tile_from_hex, get_hex_at_x_y etc.
    # We don't need a surface to generate some hexes.
    # Just generate grid, mark some hexes, simulate mousepos_x, mousepos_y and use functions
    # flat_hex_to_pixel / pixel_to_flat_hex

    # TODO: Also, generate a fixed size color map with known color sizes.
    # Then, we can calculate how much hexagons of each color there should be.
    # Because we know the size of the hexagon etc. - we can e.g. generate an image
    # that is half mountains half river (half of it is the color of river and other half of mountains)
    # Then, we calculate how much river hexes and how much mountain hexes there are.
    # These tests have to be done later!.

if __name__ == "__main__":
    unittest.main()
