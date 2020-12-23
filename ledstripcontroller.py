from injector import inject
from animationrunnerbase import AnimationRunnerBase
from animations.walk import Walk
from ledstripbase import LedstripBase


class LedstripController:
    @inject
    def __init__(self, ledstrip: LedstripBase, animation_runner: AnimationRunnerBase):
        self.__pixel_count = ledstrip.get_pixel_count()
        self.__ledstrip = ledstrip
        self.__available_animations = {"walk": lambda: Walk(self.__pixel_count)}
        self.__animation_runner = animation_runner

    def start_animation(self, animation_name):
        animation = self.__available_animations[animation_name]
        assert (animation is not None)
        self.__animation_runner.add_animation(animation())
        if not self.__animation_runner.is_running():
            self.__animation_runner.start(self.__ledstrip)

    def get_animations(self):
        animations = {}
        for animation in self.__available_animations.keys():
            animations[animation] = self.__available_animations[animation]().get_parameters()
        return animations
