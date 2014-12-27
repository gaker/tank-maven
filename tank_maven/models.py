"""
Models
"""
import bcrypt
import os
from sqlalchemy import (
    Column, String, DateTime, Boolean, Integer, Text, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlite3 import dbapi2 as sqlite
from tornado import options


Base = declarative_base()


class User(Base):
    """
    User object
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(60), nullable=False)

    def __repr__(self):
        return "<User('{0}')>".format(self.username)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())


class Configuration(Base):
    """
    Configuration object
    """
    __tablename__ = 'configuration'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    value = Column(Text, nullable=False, default={})

    def __repr__(self):
        return "<Configuration('{0}')>".format(self.name)


class InputType(Base):
    """
    Input types.
    """
    __tablename__ = 'input_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    def __repr__(self):
        return "<InputType('{0}')>".format(self.name)


class Input(Base):
    """
    Analog Input Model
    """
    __tablename__ = 'input'

    id = Column(Integer, primary_key=True)
    pin_id = Column(Integer, nullable=True)
    address_id = Column(Integer, nullable=True)
    probe_type = ForeignKey(InputType.id)
    label = Column(String(30))

    def __repr__(self):
        return "<Input('{0}: {1}')>".format(
            self.pin_id, self.probe_type)


