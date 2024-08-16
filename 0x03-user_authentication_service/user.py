#!/usr/bin/env python3
"""The `account` model's module."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Account(Base):
    """Represents a record from the `accounts` table."""
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True)
    email_address = Column(String(250), nullable=False)
    password_hash = Column(String(250), nullable=False)
    session_token = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
