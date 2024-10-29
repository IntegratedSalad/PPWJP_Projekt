import unittest
import logging
import sys
from pathlib import Path
from ..map import Hex, HexGrid

class HexGridBasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
        filename="test_results.log",
        filemode="w",
        format='%(asctime)s %(message)s',
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
        middle_hex = Hex(3, 3)
        surface_height = 500
        radius = 10
        self.hexgrid.generate_grid(middle_hex, surface_height, radius)

        self.assertIsNotNone(self.hexgrid.grid)
        self.assertIsNotNone(self.hexgrid.tiles)

        # Use the class-level logger
        self.logger.info(f"Offset Q: {self.hexgrid.offsetq}")
        self.logger.info(f"Offset R: {self.hexgrid.offsetr}")

        self.assertEqual(self.hexgrid.size, 50)
        # The second assertion is redundant and can be removed or changed
        # self.assertEqual(self.hexgrid.size, 50)

if __name__ == "__main__":
    unittest.main()
