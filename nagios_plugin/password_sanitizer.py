# -*- coding: utf-8 -*-
"""Password sanitizing utilities"""

__all__ = ['sanitize_passwords']

import re

def sanitize_set_password_syntax(msg):
    """
    Captures variations of the SET PASSWORD syntax. See:https://mariadb.com/kb/en/library/set-password/
    """
    if "SET PASSWORD" in msg.upper():
        msg = re.sub(r"=.*('|\")(\)?)", '= ***', msg, flags=re.IGNORECASE)
    return msg

def sanitize_user_identified_syntax(msg):
    """
    Captures variations of the ALTER/CREATE USER...IDENTIFIED... syntax.
    See: https://mariadb.com/kb/en/library/alter-user/
    """
    if "ALTER USER" in msg.upper() or "CREATE USER" in msg.upper():
        msg = re.sub(r"BY .*('|\")", 'BY ***', msg, flags=re.IGNORECASE)
        msg = re.sub(r"USING .*('|\")", 'USING ***', msg, flags=re.IGNORECASE)
        msg = re.sub(r"AS .*('|\")", 'AS ***', msg, flags=re.IGNORECASE)
    return msg

def sanitize_passwords(msg):
    for sanitize_fn in [sanitize_user_identified_syntax, sanitize_set_password_syntax]:
        msg = sanitize_fn(msg)
    return msg
