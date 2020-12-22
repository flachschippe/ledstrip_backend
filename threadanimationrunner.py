import threading
import time

from animationrunnerbase import AnimationRunnerBase
from ledstripbase import LedstripBase


class ThreadAnimationRunner(AnimationRunnerBase):
    def __init__(self, update_rate_in_seconds):
        super().__init__()
        self.__thread = threading.Thread(target=self.__run)
        self.__update_rate_in_seconds = update_rate_in_seconds

    def is_running(self):
        return self.__thread.is_alive()

    def _start(self):
        self.__thread.start()

    def _delay(self):
        time.sleep(self.__update_rate_in_seconds)

    def __run(self):
        while len(self._animations) > 0:
            self._run_animation()
