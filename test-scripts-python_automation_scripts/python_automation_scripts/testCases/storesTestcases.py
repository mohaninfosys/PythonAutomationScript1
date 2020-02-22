import unittest
from commonMethods import commonUtils
from testCases.storesCheckout import storesScenario


class LoginTest(unittest.TestCase):

    test = commonUtils.commonUtils()

    @staticmethod
    def setUp(utils = test):
        # Get the file location of config file
        obj = commonUtils.configObj
        # Load the config in config Object
        utils.setdriver(obj['drivers'])

    @staticmethod
    def stores():
        test = storesScenario()
        test.storesCheckout()

    @staticmethod
    def tearDownDriver(close_driver = test):
        close_driver = commonUtils.commonUtils()
        close_driver.teardown()