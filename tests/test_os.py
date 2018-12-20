import sys
import os
sys.path.append(os.path.dirname(__file__))
from utils import GreenletCalledValidatorTestCase


class AsyncOSTestCase(GreenletCalledValidatorTestCase):
    def test_chdir(self):
        from tempfile import gettempdir
        from infi.gevent_utils.os import chdir
        c = os.getcwd()
        d = gettempdir()
        self.switch_validator.assert_called(0)
        chdir(d)
        self.switch_validator.assert_called(1).tick()
        chdir(c)
        self.switch_validator.assert_called(2).tick()
        self.assertRaises(OSError, chdir, '/non_existent_dir')
        self.switch_validator.assert_called(3).tick()

    def test_fdopen(self):
        from infi.gevent_utils import os
        self.switch_validator.assert_called(0)
        fd = os.open(os.devnull, os.O_RDONLY)
        self.switch_validator.assert_called(1).tick()
        f = os.fdopen(fd)
        self.switch_validator.assert_called(2).tick()
        self.assertEqual('', f.read())
        self.switch_validator.assert_called(3).tick()
        f.close()
        self.switch_validator.assert_called(4).tick()
