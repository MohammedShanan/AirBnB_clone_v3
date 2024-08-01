#!/usr/bin/python3
"""defines a route for an API endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route("/states", methods=["Get"])
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


@app_views.route("/states", methods=["POST"])
def create_state():
    """Creates a State"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """update a State"""
    state = storage.get(State, state_id)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignored = ["id", "created_at", "updated_at"]
    update_dict = {k: v for k, v in data.items() if k not in ignored}
    for k, v in update_dict.items():
        setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
