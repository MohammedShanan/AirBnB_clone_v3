#!/usr/bin/python3
"""defines a route for an API endpoint"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage
