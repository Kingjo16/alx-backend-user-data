#!/usr/bin/env python3
"""Index view module."""

from flask import Blueprint, abort

bp = Blueprint('index', __name__)

@bp.route('/api/v1/forbidden', methods=['GET'])
def forbidden():
    """Endpoint that raises a 403 Forbidden error."""
    abort(403)

@bp.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized():
    """Endpoint that raises a 401 Unauthorized error."""
    abort(401)
