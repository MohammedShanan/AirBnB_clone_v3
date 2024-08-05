#!/usr/bin/python3
"""defines a route for an API endpoint"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"])
def get_users():
    """Retrieve all users"""
    users = storage.all(User).values()
    return jsonify([User.to_dict() for User in users])


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Retrieves a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """Creates a user"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
