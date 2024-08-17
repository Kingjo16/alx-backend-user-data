#!/usr/bin/env python3
"""Module whic encript a password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Password haser with a bytes."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a hash password is created or not and valid."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
