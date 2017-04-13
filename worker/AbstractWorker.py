from threading import Thread, Event
from abc import ABCMeta, abstractmethod


class AbstractWorker(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.thread = None
        self._stop = Event()

    @abstractmethod
    def loop_iteration(self):
        raise NotImplemented

    @abstractmethod
    def persist_packet(self, packer):
        raise NotImplemented

    def _run(self):
        while not self._stop.is_set():
            self.loop_iteration()
        self._stop.clear()
        self.thread = None

    def async_start(self):
        if self.thread is not None:
            raise Exception("cant start what is started")
        else:
            self.thread = Thread(target=self._run)
            self.thread.start()

    def stop(self):
        if self.thread is None:
            raise Exception("cant stop what is stopped")
        else:
            self._stop.set()
