"""
Utility functions
"""
import argparse
import functools
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import parse_config_file

from tank_maven.models import Base as ModelBase
from tank_maven.core.conf import settings


def setup_db():
    """
    Setup the database connection
    """
    engine = create_engine(settings.DATABASE)
    ModelBase.metadata.bind = engine
    ModelBase.metadata.create_all(engine)

    return scoped_session(sessionmaker(bind=engine))

