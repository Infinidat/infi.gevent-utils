from __future__ import absolute_import
from infi.gevent_utils.os import path

import sys
import os
sys.path.append(os.path.dirname(__file__))
from utils import GreenletCalledValidatorTestCase


class PathTestCase(GreenletCalledValidatorTestCase):
    def test_exists(self):
        self.switch_validator.assert_called(0)
        self.assertFalse(path.exists("/this_path_probably_doesnt_exist_or_else_the_test_will_fail"))
        self.switch_validator.assert_called(1)

    def test_basename(self):
        self.switch_validator.assert_called(0)
        self.assertEqual("a.text", path.basename("/a/b/c/a.text"))
        self.switch_validator.assert_called(0)
