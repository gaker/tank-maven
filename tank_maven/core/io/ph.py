"""
PH Probe control
"""
from tank_maven.core.io import Serial


class PH(Serial):
    """
    PH Probe
    """
    tty = "/dev/ttyAMA0"
    baud = 9600

