from __future__ import absolute_import
from infi.gevent_utils.tempfile import (TemporaryFile, NamedTemporaryFile, SpooledTemporaryFile, mkstemp, mkdtemp,
                                        gettempdir)

import sys
import os
sys.path.append(os.path.dirname(__file__))
from utils import GreenletCalledValidatorTestCase


class TempfileTestCase(GreenletCalledValidatorTestCase):
    def test_TemporaryFile(self):
        # We're testing that:
        # 1. simple read/write/seek functionality works
        # 2. write yields to other greenlets
        # TODO: delete reference to f and make sure there is no open file descriptor
        self.switch_validator.assert_called(0)
        f = TemporaryFile()
        self.switch_validator.assert_called(1).tick()
        f.write("hello")
        self.switch_validator.assert_called(2).tick()
        f.seek(0)  # seek isn't deferred
        self.switch_validator.assert_called(2)
        self.assertEquals("hello", f.read())
        self.switch_validator.assert_called(3)

    def test_NamedTemporaryFile(self):
        # We're testing that:
        # 1. simple read/write/seek functionality works
        # 2. we have a path under .name
        # 3. write yields to other greenlets
        # 4. deleting a reference to f deletes the file
        self.switch_validator.assert_called(0)
        f = NamedTemporaryFile()
        self.assertIsNotNone(f.name)
        self.switch_validator.assert_called(1).tick()
        f.write("hello")
        self.switch_validator.assert_called(2).tick()
        f.flush()
        self.switch_validator.assert_called(3).tick()
        with open(f.name, "r") as ff:
            self.assertEquals("hello", ff.read())
        f.seek(0)  # seek isn't deferred
        self.switch_validator.assert_called(3)
        self.assertEquals("hello", f.read())
        self.switch_validator.assert_called(4)
        name = f.name
        del f
        from os.path import exists
        self.assertFalse(exists(name))

    def test_mkstemp(self):
        self.switch_validator.assert_called(0)
        fd, t = mkstemp(suffix="blat")
        self.switch_validator.assert_called(1)
        self.assertTrue(t.endswith("blat"))
        import os
        os.close(fd)
        os.unlink(t)

    def test_mkdtemp(self):
        self.switch_validator.assert_called(0)
        d = mkdtemp(suffix="blat")
        self.switch_validator.assert_called(1)
        self.assertTrue(d.endswith("blat"))
        import os
        os.rmdir(d)

    def test_gettempdir__tempdir_is_none(self):
        import tempfile
        tempfile.tempdir = None
        self.switch_validator.assert_called(0)
        d1 = gettempdir()
        self.switch_validator.assert_called(1)
        self.assertIsNotNone(tempfile.tempdir)
        self.assertEquals(tempfile.gettempdir(), d1)

    def test_gettempdir__tempdir_is_not_none(self):
        import tempfile
        d1 = tempfile.gettempdir()
        self.switch_validator.assert_called(0)
        d2 = gettempdir()
        self.switch_validator.assert_called(0)
        self.assertEquals(d1, d2)

    def test_SpooledTemporaryFile(self):
        self.assertRaises(SpooledTemporaryFile)
