#!/usr/bin/python3
"""defines a route for an API endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route("states", methods=["Get"])
def get_states():
    """Retrieves the list of all State objects"""
    all_state = storage.all(State)
    states_list = [state.to_dict() for state in all_state.values()]
    return jsonify(states_list)


@app_views.route("states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Retrieves a state object by it's Id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a state object by it's Id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("states", methods=["POST"])
def create_state():
    data = request.get_data()
    if not request.is_json:
        abort(400, message="Not a JSON")
    if "name" not in data:
        abort(400, message="Missing name")
    state = State(**data)
    state.new()
    storage.save()
    return jsonify(state.to_dict()), 201
