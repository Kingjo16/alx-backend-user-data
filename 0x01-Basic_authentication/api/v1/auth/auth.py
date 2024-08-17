#!/usr/bin/env python3
"""Authentication module for the API.
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.
        
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.
        
        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None or not excluded_paths:
            return True

        # Ensure path always ends with a slash for consistent matching
        if path[-1] != '/':
            path += '/'

        for exclusion_path in map(lambda x: x.strip(), excluded_paths):
            # Handle wildcard (*) at the end of paths
            if exclusion_path.endswith('*'):
                if path.startswith(exclusion_path[:-1]):
                    return False
            # Handle exact path match
            elif path == exclusion_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header field from the request.
        
        Args:
            request (flask.Request): The Flask request object.
        
        Returns:
            str: The value of the 'Authorization' header, or None if not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request.
        
        Args:
            request (flask.Request): The Flask request object.
        
        Returns:
            User: The current user, or None if not implemented.
        """
        return None
