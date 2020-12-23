import os
from enum import Enum

from flask import Flask

from animationrunner.countinganimationrunner import CountingAnimationRunner
from ledstripcontroller import *
from injector import Module, provider, Injector, singleton

from animationrunner.threadanimationrunner import ThreadAnimationRunner


class RunnerType(Enum):
    BASE = 1,
    THREAD = 2,
    COUNTING = 3


class LedstripType(Enum):
    BASE = 1,
    HARDWARE = 2,
    GIF = 3


class Configuration:
    def __init__(self, pixel_count, ledstrip: LedstripType, animation_runner: RunnerType):
        self.animation_iterations = 800
        self.pixel_count = pixel_count
        self.update_rate_in_seconds = .02
        self.ledstrip_type = ledstrip
        self.animation_runner_type = animation_runner
        self.port = 8080
        self.ip = "0.0.0.0"
        self.debug = False


def configure_for_test(binder):
    configuration = Configuration(25, LedstripType.GIF, RunnerType.COUNTING)
    configuration.port = 8081
    configuration.ip = "127.0.0.1"
    configuration.debug = True
    binder.bind(Configuration, to=configuration, scope=singleton)


def configure_for_raspi(binder):
    configuration = Configuration(144, LedstripType.HARDWARE, RunnerType.THREAD)
    binder.bind(Configuration, to=configuration, scope=singleton)


class LedstripModule(Module):
    @singleton
    @provider
    def provide_ledstrip(self, configuration: Configuration) -> LedstripBase:
        if configuration.ledstrip_type == LedstripType.HARDWARE:
            from ledstrip import Ledstrip
            return Ledstrip(configuration.pixel_count)
        elif configuration.ledstrip_type == LedstripType.GIF:
            from gifwriterledstrip import GifWriterLedstrip
            return GifWriterLedstrip(configuration.pixel_count, configuration.update_rate_in_seconds)

    @singleton
    @provider
    def provide_animation_runner(self, configuration: Configuration) -> AnimationRunnerBase:
        if configuration.animation_runner_type == RunnerType.THREAD:
            return ThreadAnimationRunner(configuration.update_rate_in_seconds)
        elif configuration.animation_runner_type == RunnerType.BASE:
            return AnimationRunnerBase()
        elif configuration.animation_runner_type == RunnerType.COUNTING:
            return CountingAnimationRunner(configuration.animation_iterations)

    @singleton
    @provider
    def provide_flask(self, configuration: Configuration) -> Flask:
        return Flask(__name__, static_folder="static")


if os.getenv("LOCATION") == "local":
    injector = Injector([configure_for_test, LedstripModule()])
else:
    injector = Injector([configure_for_raspi, LedstripModule()])
