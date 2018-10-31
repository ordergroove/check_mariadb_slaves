# -*- coding: utf-8 -*-

import time
from collections import OrderedDict


class LagFormatter(object):

    PARTS_MAP = OrderedDict([
        ('hour', 'hour'),
        ('min', 'minute'),
        ('sec', 'second')
    ])

    def format(self, seconds):
        seconds = time.gmtime(int(seconds))
        parts = []

        for key in self.PARTS_MAP.keys():
            value = getattr(seconds, 'tm_{}'.format(key), 0)
            if value:
                parts.append(self._get_formatted_part(key, value))

        return ' '.join(parts)

    def _get_formatted_part(self, key, value):
        return '{} {}{}'.format(
            value,
            self.PARTS_MAP.get(key),
            's' if value > 1 else ''
        )
