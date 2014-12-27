"""
Command line interface
"""
import argparse
import os
import sys

from tank_maven.forms import ChangePasswordForm
from tank_maven.models import User
from tank_maven.core.io.ph import PH
from tank_maven.core.io.temp import Temp


def parse_options():
    """
    Parse command line options
    """
    parser = argparse.ArgumentParser(
        description='Tank Maven CLI Interface')
    parser.add_argument(
        '--settings', help='Override TANK_MAVEN_SETTINGS environment variable')
    parser.add_argument(
        '--change-password', dest='change_password',
        action='store_true', help='Change Password')
    parser.add_argument(
        '--check-ph', dest='check_ph',
        action='store_true', help="Check PH")
    parser.add_argument(
        '--check-temp', dest='check_temp',
        action='store_true', help='Check Temp')
    parser.add_argument(
        '--store-data', dest='store_data',
        action='store_false', help='Store Data in InfluxDB')
    parser.add_argument(
        '--farenheit', dest='farenheit',
        action='store_true', help='Display temp in Farenheit')

    return parser.parse_args()


def main():
    """
    Main CLI Execution
    """
    # parse command line options
    options = parse_options()

    # Get settings.
    if os.environ.get('TANK_MAVEN_SETTINGS'):
        pass
    elif options.settings:
        os.environ['TANK_MAVEN_SETTINGS'] = options.settings
    else:
        os.environ['TANK_MAVEN_SETTINGS'] = 'tank_maven.settings.local'

    from tank_maven.utils import setup_db
    db = setup_db()


    if options.change_password:
        username = raw_input('Username: ')
        if not username:
            sys.stderr.write('A username is required! Try again.\n')
            username = raw_input('Username: ')
            if not username:
                exit(1)

        user = db.query(User).filter(username == username).first()
        if not user:
            sys.stderr.write('A user with that username not found, try again!\n')
            exit(1)

        password = raw_input('Password: ')
        password1 = raw_input('Password (repeated): ')

        form = ChangePasswordForm(
            data={'password': password, 'password_confirm': password1})

    elif options.check_ph:
        ph = PH()
        data = ph.read()
        exit()

    elif options.check_temp:
        temp = Temp(farenheit=options.farenheit)
        data = temp.read()

