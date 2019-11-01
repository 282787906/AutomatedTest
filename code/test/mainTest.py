import logging
import os
import sys
import traceback
import unittest

from tools import log


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
def aa():
    bb()


def bb():
    cc()


def cc():
    dd()


def dd():
    int("wer")


if __name__ == '__main__':
    try:

        aa()

    except:
        log.exception()

    log.i('asdasd')
