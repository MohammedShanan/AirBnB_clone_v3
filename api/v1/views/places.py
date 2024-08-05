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


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Retrieves a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_places(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_city_place(city_id):
    """Create a places in the city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    data.update({"city_id": city_id})
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
