# -*- coding: utf-8 -*-

import time
from collections import OrderedDict

PARTS_MAP = OrderedDict([
    ('hour', 'hour'),
    ('min', 'minute'),
    ('sec', 'second')
])


def format_lag(seconds):
    seconds = time.gmtime(int(seconds))
    parts = []

    for key in PARTS_MAP.keys():
        value = getattr(seconds, 'tm_{}'.format(key), 0)
        if value:
            formatted_part = '{} {}{}'.format(
                value,
                PARTS_MAP.get(key),
                's' if value > 1 else ''
            )
            parts.append(formatted_part)

    return ' '.join(parts)
