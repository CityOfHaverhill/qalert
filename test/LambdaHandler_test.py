import unittest
from main.LambdaHandler import LambdaHandler


class LambdaHandlerTest(unittest.TestCase):
    def set_up(self):
        print("setUp...")

    def tear_down(self):
        print("tearDown...")

    def test_returns_request(self):
        hdl = LambdaHandler()
        result = hdl.handle(None, None)
        self.assertEqual(result, "I'm a Lambda!", 'Expected other value...')
