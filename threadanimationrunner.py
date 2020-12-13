import threading
import time

from animationrunnerbase import AnimationRunnerBase
from ledstripbase import LedstripBase


class ThreadAnimationRunner(AnimationRunnerBase):
    def __init__(self):
        super().__init__()
        self.__thread = threading.Thread(target=self._run_animation)

    def is_running(self):
        return self.__thread.is_alive()

    def _start(self):
        self.__thread.start()

    def _delay(self):
        time.sleep(.2)
