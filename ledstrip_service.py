import os

from flask import Flask, jsonify
from flask_restful import Resource, reqparse, Api
from ledstripcontroller import *
from injector import Module, provider, Injector, inject, singleton

TGS = Flask(__name__)
api = Api(TGS)


class Configuration:
    def __init__(self, ledstrip):
        self.ledstrip = ledstrip


def configure_for_test(binder):
    configuration = Configuration(LedstripBase(144))
    binder.bind(Configuration, to=configuration, scope=singleton)

def configure_for_raspi(binder):
    from ledstrip import Ledstrip
    configuration = Configuration(Ledstrip(144))
    binder.bind(Configuration, to=configuration, scope=singleton)


class LedstripModule(Module):
    @singleton
    @provider
    def provide_ledstrip(self, configuration: Configuration) -> LedstripBase:
        return configuration.ledstrip

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
