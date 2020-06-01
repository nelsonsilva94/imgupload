import unittest

from flask import Flask
from flask_testing import TestCase
import urllib3

from app import sumnum


class MyTest(TestCase):

    def testsum(self):
        result = sumnum(3, 4)
        self.assertEqual(result, 8)

# your test cases


if __name__ == '__main__':
    unittest.main()