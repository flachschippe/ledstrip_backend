import os
from enum import Enum
from flask import Flask, jsonify
from flask_restful import Resource, reqparse, Api
from ledstripcontroller import *
from injector import Module, provider, Injector, inject, singleton

from threadanimationrunner import ThreadAnimationRunner

TGS = Flask(__name__)
api = Api(TGS)


class RunnerType(Enum):
    BASE = 1,
    THREAD = 2


class LedstripType(Enum):
    BASE = 1,
    HARDWARE = 2


class Configuration:
    def __init__(self, pixel_count, ledstrip: LedstripType, animation_runner: RunnerType):
        self.pixel_count = pixel_count
        self.ledstrip_type = ledstrip
        self.animation_runner_type = animation_runner


def configure_for_test(binder):
    configuration = Configuration(100, LedstripType.BASE, RunnerType.THREAD)
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
        elif configuration.ledstrip_type == LedstripType.BASE:
            return LedstripBase(configuration.pixel_count)

    @singleton
    @provider
    def provide_animation_runner(self, configuration: Configuration) -> AnimationRunnerBase:
        if configuration.animation_runner_type == RunnerType.THREAD:
            return ThreadAnimationRunner()
        elif configuration.ledstrip_type == LedstripType.BASE:
            return AnimationRunnerBase()



if os.getenv("LOCATION") == "local":
    injector = Injector([configure_for_test, LedstripModule()])
else:
    injector = Injector([configure_for_raspi, LedstripModule()])

ledstrip = injector.get(LedstripController)


class Led(Resource):
    def get(self, led):
        return jsonify({'message': 'hello world'}), 201

    def put(self, led):
        parser = reqparse.RequestParser()
        parser.add_argument("red")
        parser.add_argument("green")
        parser.add_argument("blue")
        args = parser.parse_args()
        print(args)
        value = Color(int(args["red"]), int(args["green"]), int(args["blue"]))
        ledstrip.set_pixel(led, value)
        return args, 201


class Animation(Resource):

    def put(self, animation_name):
        parser = reqparse.RequestParser()
        parser.add_argument("mode")
        ledstrip.start_animation("walk")
        args = parser.parse_args()
        return {}, 201


api.add_resource(Led, "/led/<int:led>")
api.add_resource(Animation, "/animation/<string:animation_name>")

TGS.run(debug=True, port=8080, host="0.0.0.0")
