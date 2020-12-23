from flask import Flask, request
from flask_restful import Resource, reqparse, Api

from configuration import Configuration
from ledstripcontroller import *


class LedstripService:
    @inject
    def __init__(self, ledstrip: LedstripController, flask_app: Flask, config: Configuration):
        self.__ledstrip = ledstrip
        self.__flask_app = flask_app
        self.__api = Api(flask_app)
        self.__config = config
        self.__api.add_resource(Led, "/led/<int:led>", resource_class_args= [self.__ledstrip])
        self.__api.add_resource(Animation, "/animation/<string:animation_name>", resource_class_args=[self.__ledstrip])
        self.__api.add_resource(Animations, "/animations", resource_class_args=[self.__ledstrip])

    def run(self):
        self.__flask_app.run(debug=self.__config.debug, port=self.__config.port, host=self.__config.ip)


class Led(Resource):
    def __init__(self, ledstrip: LedstripBase):
        self.__ledstrip = ledstrip

    def get(self, led):
        return {'message': 'hello world'}, 201

    def put(self, led):
        parser = reqparse.RequestParser()
        parser.add_argument("red")
        parser.add_argument("green")
        parser.add_argument("blue")
        args = parser.parse_args()
        print(args)
        value = Color(int(args["red"]), int(args["green"]), int(args["blue"]))
        self.__ledstrip.set_pixel(led, value)
        return args, 201


class Animations(Resource):
    def __init__(self, ledstrip: LedstripBase):
        self.__ledstrip = ledstrip

    def get(self):
        animations = {}
        available_animations = {}
        for animation in self.__ledstrip.get_available_animations():
            available_animations[animation.get_name()] = animation.get_parameters()
        animations["available_animations"] = available_animations

        active_animations = {}
        for animation_id, animation in self.__ledstrip.get_active_animations().items():
            active_animations[animation_id] = {animation.get_name(): animation.get_parameters()}
        animations["active_animations"] = active_animations
        return animations


class Animation(Resource):
    def __init__(self, ledstrip: LedstripBase):
        self.__ledstrip = ledstrip

    def post(self, animation_name):
        parser = reqparse.RequestParser()
        args = request.get_json()
        animation_id = self.__ledstrip.start_animation(animation_name)
        return {"animation_id": animation_id}, 201
