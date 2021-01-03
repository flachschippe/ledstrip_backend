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
        self.__available_animations = {walk.get_name(): walk, "w2": walk}
        self.__animation_runner = animation_runner

    def start_animation(self, animation_name, parameters):
        animation = self.__available_animations[animation_name]
        assert(animation is not None)
        new_animation = animation.clone()
        new_animation.set_parameters(parameters)
        animation_id = self.__animation_runner.add_animation(new_animation)
        if not self.__animation_runner.is_running():
            self.__animation_runner.start(self.__ledstrip)
        return animation_id

    def remove_animation(self, animation_id):
        self.__animation_runner.remove_animation(animation_id)

    def get_available_animations(self):
        return self.__available_animations.values()

    def get_active_animations(self):
        return self.__animation_runner.get_animations()

