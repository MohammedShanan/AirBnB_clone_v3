#!/usr/bin/python3
"""defines a route for an API endpoint"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_city_places(city_id):
    """Retrieves all places in the city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])
