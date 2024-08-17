#!/usr/bin/env python3
"""Base module.
"""
import json
import uuid
from os import path
from datetime import datetime
from typing import TypeVar, List, Iterable


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base:
    """Base class for managing data storage and serialization."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance with ID, timestamps, and data management."""
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = datetime.strptime(kwargs.get('created_at'), TIMESTAMP_FORMAT) if kwargs.get('created_at') else datetime.utcnow()
        self.updated_at = datetime.strptime(kwargs.get('updated_at'), TIMESTAMP_FORMAT) if kwargs.get('updated_at') else datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Check if two objects are equal based on type and ID."""
        return isinstance(other, Base) and self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """Convert object to JSON-compatible dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            result[key] = value.strftime(TIMESTAMP_FORMAT) if isinstance(value, datetime) else value
        return result

    @classmethod
    def load_from_file(cls):
        """Load all objects from a JSON file."""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """Save all objects to a JSON file."""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {obj_id: obj.to_json(True) for obj_id, obj in DATA[s_class].items()}

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """Save the current object and update timestamps."""
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Remove the current object from storage."""
        s_class = self.__class__.__name__
        if self.id in DATA[s_class]:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Return the total count of stored objects."""
        return len(DATA[cls.__name__])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Return all stored objects."""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Retrieve an object by ID."""
        return DATA[cls.__name__].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search for objects matching specified attributes."""
        def _search(obj):
            return all(getattr(obj, k) == v for k, v in attributes.items()) if attributes else True

        return list(filter(_search, DATA[cls.__name__].values()))
