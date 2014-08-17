import gevent
from unittest import TestCase
from infi.gevent_utils.gevent_loop import GeventLoopBase, loop_in_background


class GeventLoopTestCase(TestCase):
    def test_loop_in_background(self):
        iters = []

        def foo():
            iters.append(1)

        with loop_in_background(0.1, foo):
            gevent.sleep(0.3)

        self.assertTrue(2 <= len(iters) <= 4)

    def test_loop_in_background_abort(self):
        iters = []

        def foo():
            iters.append(1)

        with loop_in_background(0.1, foo) as loop:
            gevent.sleep(0.1)
            loop.stop()

        self.assertTrue(1 <= len(iters) <= 2)

    def test_loop__join_timeout(self):
        class Loopy(GeventLoopBase):
            def _loop_callback(self):
                pass

        loopy = Loopy(0.1)
        loopy.start()
        self.assertFalse(loopy.join(0.2))
        loopy.kill()

    def test_loop__stop_inside_loop(self):
        class Loopy(GeventLoopBase):
            def _loop_callback(self):
                self.stop()

        loopy = Loopy(0.1)
        loopy.start()
        self.assertTrue(loopy.join(0.2))
