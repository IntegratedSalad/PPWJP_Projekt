import unittest
import logging
from fsm import FSM

class FSMBasicTest(unittest.TestCase):

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

        cls.logger = logging.getLogger("FSMBasicTest")
        cls.logger.setLevel(logging.DEBUG)
        cls.fh = logging.FileHandler('test_results.log')
        cls.fh.setLevel(logging.DEBUG)
        cls.fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
        cls.logger.addHandler(cls.fh)

        cls.fsm = FSM()

    def setUp(self):
        # self.//
        # TODO: Setup state transitions
        pass
    
    def test_state_change_from_STATE_LOOKING_FOR_FOOD_to_STATE_EATING(self):
        pass


