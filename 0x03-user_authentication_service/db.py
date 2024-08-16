#!/usr/bin/env python3
"""Database management module for account from the users records."""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from account import Base, Account


class Database:
    """Database class for managing account records."""

    def __init__(self) -> None:
        """Initialize a new Database instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_account(self, email_address: str, password_hash: str) -> Account:
        """Adds a new account to the database."""
        try:
            new_account = Account(email_address=email_address, password_hash=password_hash)
            self._session.add(new_account)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_account = None
        return new_account

    def find_account_by(self, **kwargs) -> Account:
        """Finds an account based on a set of filters."""
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(Account, key):
                fields.append(getattr(Account, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(Account).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_account(self, account_id: int, **kwargs) -> None:
        """Updates an account based on a given ID."""
        account = self.find_account_by(account_id=account_id)
        if account is None:
            return
        update_data = {}
        for key, value in kwargs.items():
            if hasattr(Account, key):
                update_data[getattr(Account, key)] = value
            else:
                raise ValueError()
        self._session.query(Account).filter(Account.account_id == account_id).update(
            update_data,
            synchronize_session=False,
        )
        self._session.commit()
