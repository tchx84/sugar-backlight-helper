import os
import logging

from functools import cmp_to_key
from gi.repository import GUdev


class Device:

    def __init__(self):
        self._path = None
        self._type = None
        self._get_best_backlight()

    def _get_best_backlight(self):
        client = GUdev.Client()
        devices = client.query_by_subsystem('backlight')

        if not devices:
            logging.error('No devices were found.')
            return

        devices.sort(key=cmp_to_key(Device._sort_criteria))
        self._path = devices[0].get_sysfs_path()
        self._type = devices[0].get_sysfs_attr('type')

        logging.info('Found device at %s', self._path)

    @staticmethod
    def _sort_criteria(ldevice, rdevice):
        if ldevice.get_sysfs_attr('type') == 'firmware':
            return 1
        if ldevice.get_sysfs_attr('type') == 'platform' and \
           rdevice.get_sysfs_attr('type') == 'raw':
            return 1
        return -1

    def _read_file(self, path):
        try:
            with open(path) as file:
                return int(file.read())
        except IOError:
            logging.error('Could not read from %s.', path)
            return None

    def get_brightness(self):
        path = os.path.join(self._path, 'brightness')
        return self._read_file(path)

    def get_max_brightness(self):
        path = os.path.join(self._path, 'max_brightness')
        return self._read_file(path)

    def set_brightness(self, value):
        max_value = self.get_max_brightness()
        if not max_value:
            logging.error('Could not get maximum value for %s', self._path)
            return

        if self._type == 'raw':
            if max_value > 99:
                minimum = 1
            else:
                minimum = 0
            value = max(minimum, value)

        path = os.path.join(self._path, 'brightness')
        try:
            with open(path, 'w') as file:
                file.write(str(value))
        except IOError:
            logging.error('Could not write %d to %s.', value, path)

device = Device()
print device.get_brightness()
max_brightness = device.get_max_brightness()
print max_brightness
device.set_brightness(max_brightness)
