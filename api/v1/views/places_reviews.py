#!/usr/bin/python3
"""defines a route for an API endpoint"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_place_reviews(place_id):
    """Retrieves all reviews for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """Retrieves a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Create a review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")
    data.update({"place_id": place_id})
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
