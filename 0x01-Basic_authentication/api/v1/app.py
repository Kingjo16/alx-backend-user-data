#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify
from api.v1.views import index

app = Flask(__name__)
app.register_blueprint(index.bp)

@app.errorhandler(401)
def unauthorized_error(error):
    """Handle 401 Unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
