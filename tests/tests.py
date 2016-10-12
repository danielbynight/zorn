import unittest

from .cli import StartProjectTest

suite = unittest.TestSuite()


if __name__ == '__main__':
    suite.addTest(StartProjectTest)