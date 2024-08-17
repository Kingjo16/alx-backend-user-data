#!/usr/bin/env python3
"""User module.
"""
import hashlib
from models.base import Base


class User(Base):
    """User model handling user-related data and logic."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance with basic details."""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Get the hashed password."""
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Set and hash a new password using SHA256.

        Note: Use a stronger hashing algorithm like argon2 or bcrypt for production.
        """
        if not pwd or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """Check if the given password matches the stored hash."""
        if not pwd or not isinstance(pwd, str):
            return False
        return hashlib.sha256(pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Return a user-friendly name based on available data."""
        if not any([self.email, self.first_name, self.last_name]):
            return ""
        if not self.first_name and not self.last_name:
            return self.email
        if not self.last_name:
            return self.first_name
        if not self.first_name:
            return self.last_name
        return f"{self.first_name} {self.last_name}"
