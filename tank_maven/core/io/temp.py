"""
Check Temp
"""
from tank_maven.core.io import Analog


class Temp(Analog):
    """
    Check temp.
    """
    farenheit = False

    def __init__(self, farenheit=False):
        super(Temp, self).__init__()
        self.farenheit = farenheit

    def read(self):
        """
        Get the temp
        """
        probe = super(Temp, self).read()

        temp = 0.0512 * (0.0048 * probe * 1000) - 20.5128
        temp = Decimal(temp)

        if self.farenheit:
             temp = ((temp * 9) / 5) + 32

        # format the temp
        return format(temp, '.2f')

