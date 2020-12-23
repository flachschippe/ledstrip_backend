from injector import inject
from animationrunner.animationrunnerbase import AnimationRunnerBase
from animations import Walk
from ledstripbase import LedstripBase


class LedstripController:
    @inject
    def __init__(self, ledstrip: LedstripBase, animation_runner: AnimationRunnerBase):
        self.__pixel_count = ledstrip.get_pixel_count()
        self.__ledstrip = ledstrip
        walk = Walk(self.__pixel_count)
        self.__available_animations = {walk.get_name(): walk}
        self.__animation_runner = animation_runner

    def start_animation(self, animation_name):
        animation = self.__available_animations[animation_name]
        assert(animation is not None)
        self.__animation_runner.add_animation(animation.clone())
        if not self.__animation_runner.is_running():
            self.__animation_runner.start(self.__ledstrip)

    def get_animations(self):
        animations = {"available_animations":[], "active_animations":[]}
        for animation in self.__available_animations.values():
            animations["available_animations"].append({animation.get_name(): animation.get_parameters()})

        active_animations = self.__animation_runner.get_animations()
        for animation in active_animations:
            animations["active_animations"].append({animation.get_name(): animation.get_parameters()})
        return animations
