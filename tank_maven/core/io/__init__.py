"""
Control IO
"""
import serial
import spidev
import sys

from decimal import Decimal
from influxdb import InfluxDBClient


class IO(object):
    """
    Base class for IO Controls
    """
    pin = None

    def read(self):
        """
        Read the IO
        """
        raise NotImplementedError('Subclasses must implement')


class Serial(IO):
    """
    Serial port.
    """
    tty = None
    baud = None

    def __init__(self):
        if not self.tty and not self.baud:
            raise Exception('TTY and baud are required')

        try:
            self.serial = serial.Serial(self.tty, self.baud)
        except OSError, e:
            exit()

    def read(self):
        """
        Read data from ``self.tty``
        """
        while True:
            line = ""
            data = self.serial.read()
            if data == "\r":
                return line
            else:
                line = line + data


class Analog(IO):
    """
    Check an analog probe.
    """
    bus = None
    device = None

    def __init__(self):
        """
        Setup ``SpiDev()``
        """
        if not self.bus and self.device:
            raise Exception('Bus and device are required in subclasses')

        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)

    def read(self):
        """
        Read the input
        """
        r = spi.xfer2([1, (8 + 0) << 4, 0])
        return ((r[1] & 3) << 8) + r[2]

