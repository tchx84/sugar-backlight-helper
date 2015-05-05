#!/usr/bin/env python2

# Copyright (C) 2015, Martin Abente Lahaye - tch@sugarlabs.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
from argparse import ArgumentParser
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
            print 'No devices were found.'
            return

        devices.sort(key=cmp_to_key(Device._sort_criteria))
        self._path = devices[0].get_sysfs_path()
        self._type = devices[0].get_sysfs_attr('type')

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
            print 'Could not read from %s.' % path
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
            print 'Could not get maximum value for %s' % self._path
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
            print 'Could not write %d to %s.' % (value, path)


def _main():
    parser = ArgumentParser()
    parser.add_argument('--get-brightness',
                        dest="get_brightness",
                        default=False,
                        action='store_true',
                        help='Get the current brightness')
    parser.add_argument('--get-max-brightness',
                        dest="get_max_brightness",
                        default=False,
                        action='store_true',
                        help='Get the number of brightness levels supported')
    parser.add_argument('--set-brightness',
                        dest="set_brightness",
                        default=None,
                        type=int,
                        help='Set the current brightness')

    args = parser.parse_args()
    if args.get_brightness is False and \
       args.get_max_brightness is False and \
       args.set_brightness is None:
        print parser.error('No valid option was specified')

    device = Device()
    if args.get_brightness is True:
        print device.get_brightness()
    elif args.get_max_brightness is True:
        print device.get_max_brightness()
    elif args.set_brightness is not None:
        device.set_brightness(int(args.set_brightness))

if __name__ == '__main__':
    _main()
