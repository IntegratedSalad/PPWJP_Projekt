import unittest
import logging
import bear
import map

class BearsBehaviorBasicTest(unittest.TestCase):

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

        cls.logger = logging.getLogger("BearsBehaviorBasicTest")
        cls.logger.setLevel(logging.DEBUG)
        cls.fh = logging.FileHandler('test_results.log')
        cls.fh.setLevel(logging.DEBUG)
        cls.fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
        cls.logger.addHandler(cls.fh)

    def setUp(self):
        # self.//
        # TODO: Setup Bears and map
        pass

    def test_start_looking_for_food(self):
        pass