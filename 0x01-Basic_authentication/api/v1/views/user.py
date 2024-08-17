#!/usr/bin/env python3
"""User views module.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Returns:
      - JSON list of all User objects.
    """
    return jsonify([user.to_json() for user in User.all()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str) -> str:
    """GET /api/v1/users/<user_id>
    Returns:
      - JSON representation of a User object.
      - 404 if the User ID doesn't exist.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """DELETE /api/v1/users/<user_id>
    Returns:
      - Empty JSON if the User is deleted.
      - 404 if the User ID doesn't exist.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users
    JSON body:
      - email (required).
      - password (required).
      - first_name (optional).
      - last_name (optional).
    Returns:
      - JSON representation of the created User.
      - 400 if the request is improperly formatted or missing fields.
    """
    try:
        rj = request.get_json()
        if not rj:
            return jsonify({'error': 'Wrong format'}), 400
        if not rj.get('email'):
            return jsonify({'error': 'email missing'}), 400
        if not rj.get('password'):
            return jsonify({'error': 'password missing'}), 400

        user = User(
            email=rj.get('email'),
            password=rj.get('password'),
            first_name=rj.get('first_name'),
            last_name=rj.get('last_name')
        )
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> str:
    """PUT /api/v1/users/<user_id>
    JSON body:
      - first_name (optional).
      - last_name (optional).
    Returns:
      - JSON representation of the updated User.
      - 404 if the User ID doesn't exist.
      - 400 if the request is improperly formatted.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
        if not rj:
            return jsonify({'error': 'Wrong format'}), 400

        user.first_name = rj.get('first_name', user.first_name)
        user.last_name = rj.get('last_name', user.last_name)
        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400
