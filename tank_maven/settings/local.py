import os
from tank_maven.settings.base import *

DEBUG = True

db_dir = os.path.join(BASE_DIR, 'tmp')

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

DATABASE = 'sqlite:///{0}'.format(os.path.join(db_dir, 'db.sql'))

