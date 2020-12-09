import time
from flask import Flask, jsonify
from flask_restful import Resource, reqparse, Api
from ledstrip import *

TGS = Flask(__name__)
api = Api(TGS)

ledstrip = Ledstrip(144, 18)

walk = Walk(ledstrip)
walk.start()
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
    return args  , 201

api.add_resource(Led, "/led/<int:led>")

TGS.run(debug=True,port=8080,host="0.0.0.0")


time.sleep(1000)