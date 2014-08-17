import os
from unittest import TestCase


class AsyncOSTestCase(TestCase):
    def test_chdir(self):
        from tempfile import gettempdir
        from infi.gevent_utils.os import chdir
        c = os.getcwd()
        d = gettempdir()
        chdir(d)
        chdir(c)
        self.assertRaises(OSError, chdir, '/non_existant_dir')
