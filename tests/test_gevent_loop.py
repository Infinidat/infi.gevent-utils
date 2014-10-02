import gevent
from unittest import TestCase
from functools import partial
from infi.gevent_utils.gevent_loop import GeventLoopBase, GeventLoop, loop_in_background


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

    def test_loop__stop_inside_loop(self):
        class Loopy(GeventLoopBase):
            def _loop_callback(self):
                self.stop()

        loopy = Loopy(0.1)
        loopy.start()
        self.assertTrue(loopy.stop(0.2))

    def test_loop__kill_inside_loop(self):
        loopy = GeventLoop(0.01, partial(gevent.sleep, 10))
        loopy.start()
        gevent.sleep(0.1)  # make sure the loop starts
        loopy._greenlet.kill()
        self.assertFalse(loopy.has_started())

    def test_loop__repr(self):
        repr(GeventLoop(1, lambda: True))
