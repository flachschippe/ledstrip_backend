from flask import Flask, request
from flask_restful import Resource, reqparse, Api

from animations.parameter.colorparameter import ColorParameter
from animations.parameter.integerparameter import IntegerParameter
from configuration import Configuration
from ledstripcontroller import *


class LedstripService:
    @inject
    def __init__(self, ledstrip: LedstripController, flask_app: Flask, config: Configuration):
        self.__ledstrip = ledstrip
        self.__flask_app = flask_app
        self.__api = Api(flask_app)
        self.__config = config
        self.__flask_app.after_request(LedstripService.set_header)
        self.__api.add_resource(Animation, "/animation/<int:animation_id>", "/animation", resource_class_args=[self.__ledstrip])
        self.__api.add_resource(Animations, "/animations", resource_class_args=[self.__ledstrip])

    def run(self):
        self.__flask_app.run(debug=self.__config.debug, port=self.__config.port, host=self.__config.ip)

    @staticmethod
    def set_header(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        return response


class Animations(Resource):
    def __init__(self, ledstrip: LedstripBase):
        self.__ledstrip = ledstrip

    def get(self):
        animations = {}
        available_animations = []
        for animation in self.__ledstrip.get_available_animations():
            available_animations.append({"name": animation.get_name(),
                                         "parameters": {n: p.to_dict() for n, p in animation.get_parameters().items()}})
        animations["available_animations"] = available_animations

        active_animations = []
        for animation_id, animation in self.__ledstrip.get_active_animations().items():
            active_animations.append({"id": animation_id,
                                      "name": animation.get_name(),
                                      "parameters": {n: p.to_dict() for n, p in animation.get_parameters().items()}})
        animations["active_animations"] = active_animations
        return animations


class Animation(Resource):
    def __init__(self, ledstrip: LedstripBase):
        self.__ledstrip = ledstrip

    def post(self):
        args = request.get_json()

        request_parameters = args["parameters"]
        parameters = {}
        animation_name = args["name"]
        for parameter in request_parameters:
            if parameter["type"] == "integer":
                parameters[parameter["name"]] = IntegerParameter.from_string(parameter["value"])
            if parameter["type"] == "color":
                parameters[parameter["name"]] = ColorParameter.from_string(parameter["value"])
        animation_id = self.__ledstrip.start_animation(animation_name, parameters)
        return {"animation_id": animation_id}, 201

    def delete(self, animation_id):
        self.__ledstrip.remove_animation(animation_id)
        return {"animation_id": animation_id}, 201
