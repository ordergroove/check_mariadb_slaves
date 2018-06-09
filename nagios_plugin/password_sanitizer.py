# -*- coding: utf-8 -*-
"""Password sanitizing utilities"""

__all__ = ['sanitize_passwords']

import re

def sanitize_set_password_syntax(msg):
    """
    Captures variations of the SET PASSWORD syntax. See:https://mariadb.com/kb/en/library/set-password/
    """
    if "SET PASSWORD" in msg.upper():
        return re.sub(r"=.*('|\")(\)?)", '= ***', msg)
    return msg

def sanitize_passwords(msg):
    return sanitize_set_password_syntax(msg)
