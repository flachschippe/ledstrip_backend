from animationrunner import AnimationRunnerBase


class CountingAnimationRunner(AnimationRunnerBase):
    def __init__(self, iterations):
        super().__init__()
        self.__iterations = iterations
        self.__is_running = False

    def is_running(self):
        return self.__is_running

    def _start(self):
        self.__is_running = True
        for i in range(0, self.__iterations):
            self._run_animation()
        self._ledstrip.shutdown()

    def _delay(self):
        pass
