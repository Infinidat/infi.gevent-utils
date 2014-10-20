import sys
import os
sys.path.append(os.path.dirname(__file__))
from utils import GreenletCalledValidatorTestCase


class DeferredTestCase(GreenletCalledValidatorTestCase):
    def test_func_with_doc(self):
        from infi.gevent_utils.deferred import create_threadpool_executed_func

        def foo():
            """my_doc"""
            pass

        _foo = create_threadpool_executed_func(foo)
        self.assertEquals(_foo.__doc__, "(gevent-friendly) my_doc")

    def test_func_without_doc(self):
        from infi.gevent_utils.deferred import create_threadpool_executed_func

        def foo():
            pass

        _foo = create_threadpool_executed_func(foo)
        self.assertEquals(_foo.__doc__, "(gevent-friendly)")

    def test_func_exception(self):
        from infi.gevent_utils.deferred import create_threadpool_executed_func

        def foo():
            raise Exception("blat")

        _foo = create_threadpool_executed_func(foo)
        self.switch_validator.assert_called(0)
        self.assertRaises(Exception, _foo)
        self.switch_validator.assert_called(1).tick()
