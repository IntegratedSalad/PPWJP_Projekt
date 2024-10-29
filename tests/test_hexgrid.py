import unittest
from ..map import Hex, HexGrid

class DefaultTest(unittest.TestCase):

    def setUp(self):
        self.radius = 0
        self.hexgrid = HexGrid(self.radius)
        # self.middle_hex = Hex()

    def test_generating_grid(self):
        # self.hexgrid.generate_grid()
        self.assertEqual(self.hexgrid.radius, 0)
        

if __name__ == "__main__":
    unittest.main()