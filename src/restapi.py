# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from marshmallow import Schema, fields, post_load

import tidegravity as tg

app = Flask(__name__)
api = Api(app)


class Location:
    def __init__(self, **kwargs):
        self.lat = kwargs.get('lat')
        self.lon = kwargs.get('lon')
        self.alt = kwargs.get('alt', 0)

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        return '<Location lat(%.4f) lon(%.4f) alt(%.4f)>' % (self.lat, self.lon, self.alt)


class LocationSchema(Schema):
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    alt = fields.Float(required=False, default=0)

    @post_load
    def make_location(self, data):
        return Location(**data)


class Tide(Resource):
    """
    Tide Resource which provides a GET and POST method, allowing simple requests for the current tide using
    query string parameters, or by POSTing a JSON encoded request object with Latitude (lat), Longitude (lon),
    and optionally Altitude (alt)
    """
    def get(self):
        query = {key: request.args[key] for key in request.args}
        errors = LocationSchema().validate(query)
        if errors:
            return jsonify({"success": False, "msg": errors})

        loc = LocationSchema().load(query).data

        dt = datetime.utcnow()
        gm, gs, g0 = tg.solve_longman_tide_scalar(**loc, time=dt)

        return jsonify({"success": True, "gm": gm, "gs": gs, "g0": g0, "t0": dt.isoformat()})

    def post(self):
        if request.json is None:
            return jsonify({"success": False, "msg": "No JSON Payload found."})
        errors = LocationSchema().validate(request.json)
        if errors:
            return jsonify({"success": False, "msg": errors})

        loc = LocationSchema().load(request.json).data

        dt = datetime.utcnow()
        gm, gs, g0 = tg.solve_longman_tide_scalar(**loc, time=dt)

        return jsonify({"success": True, "gm": gm, "gs": gs, "g0": g0, "t0": dt.isoformat()})


api.add_resource(Tide, '/v1/tide/')
