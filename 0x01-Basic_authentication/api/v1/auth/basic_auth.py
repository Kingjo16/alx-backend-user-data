#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar, Optional
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class.
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> Optional[str]:
        """Extracts the Base64 part of the Authorization header
        for a Basic Authentication.

        Args:
            authorization_header (str): The authorization header.

        Returns:
            Optional[str]: The Base64 encoded part of the header, or None.
        """
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> Optional[str]:
        """Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            Optional[str]: The decoded string, or None if decoding fails.
        """
        if isinstance(base64_authorization_header, str):
            try:
                decoded_bytes = base64.b64decode(
                    base64_authorization_header,
                    validate=True
                )
                return decoded_bytes.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """Extracts user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.

        Args:
            decoded_base64_authorization_header (str): The decoded authorization header.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the user and password, or (None, None).
        """
        if isinstance(decoded_base64_authorization_header, str):
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(pattern, decoded_base64_authorization_header.strip())
            if field_match:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> Optional[TypeVar('User')]:
        """Retrieves a user based on the user's authentication credentials.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            Optional[User]: The User object if credentials are valid, None otherwise.
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if users and users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """Retrieves the user from a request.

        Args:
            request (flask.Request): The request object.

        Returns:
            Optional[User]: The authenticated user, or None if authentication fails.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        if b64_auth_token:
            auth_token = self.decode_base64_authorization_header(b64_auth_token)
            if auth_token:
                email, password = self.extract_user_credentials(auth_token)
                if email and password:
                    return self.user_object_from_credentials(email, password)
        return None
