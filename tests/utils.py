import gevent
import gevent.event
from unittest import TestCase


class GreenletCalledValidator(object):
    def __init__(self, spawn=True):
        self.call_counter = 0
        self.greenlet = None
        self.event = gevent.event.Event()
        if spawn:
            self.spawn()

    def spawn(self):
        self.greenlet = gevent.spawn(self._execute)
        assert self.call_counter == 0

    def done(self):
        self.greenlet.kill()

    def assert_called(self, counter):
        assert self.call_counter == counter, "call counter error (expected: {}, got: {})".format(counter, self.call_counter)
        return self

    def tick(self):
        self.event.set()

    def _execute(self):
        while True:
            self.call_counter = self.call_counter + 1
            self.event.wait()
            self.event.clear()


class GreenletCalledValidatorTestCase(TestCase):
    def setUp(self):
        super(GreenletCalledValidatorTestCase, self).setUp()
        self.switch_validator = GreenletCalledValidator()

    def tearDown(self):
        self.switch_validator.done()
        super(GreenletCalledValidatorTestCase, self).tearDown()
