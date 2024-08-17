#!/usr/bin/env python3
"""Index view routes.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Returns:
      - API status in JSON format.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Returns:
      - Object count stats in JSON format.
    """
    from models.user import User
    stats = {'users': User.count()}
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """GET /api/v1/unauthorized
    Triggers a 401 error for unauthorized access.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """GET /api/v1/forbidden
    Triggers a 403 error for forbidden access.
    """
    abort(403)
