import time
import threading
from threading import Thread

class Scheduler(Thread):
    def_sleep = 5
    def __init__(self):
        super(Scheduler, self).__init__()
        self._stop_event = threading.Event()
        self.scheduled = []

    def run(self):
        try:
            sleep = Scheduler.def_sleep
            while (len(self.scheduled) != 0 or sleep != 0):
                if (len(self.scheduled) != 0):
                    curr = self.scheduled[0]
                    if time.time() - curr['start'] >= curr['limit']:
                        curr['func']()
                        self.scheduled.pop(0)
                        continue
                    time.sleep(curr['limit'] - (time.time() - curr['start']))
                else:
                    time.sleep(Scheduler.def_sleep)
                    sleep = 0
        finally:
            self.stop()

    def add_event(self, run_in, function):
        now = time.time()
        self.scheduled.append({
            'start': now,
            'limit': run_in,
            'func': function
        })

    def stop(self):
        self._stop_event.set()