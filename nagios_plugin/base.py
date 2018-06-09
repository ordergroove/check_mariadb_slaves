# -*- coding: utf-8 -*-
"""Nagios Plugin base class"""

__all__ = ['NagiosPlugin']

import sys


class NagiosPlugin(object):
    def __init__(self, warning, critical, *args, **kwargs):
        self.warning = warning
        self.critical = critical

    def run_check(self):
        raise NotImplementedError

    @staticmethod
    def ok_state(msg):
        print "OK - {0}".format(msg)
        sys.exit(0)

    @staticmethod
    def warning_state(msg):
        print "WARNING - {0}".format(msg)
        sys.exit(1)

    @staticmethod
    def critical_state(msg):
        print "CRITICAL - {0}".format(msg)
        sys.exit(2)

    @staticmethod
    def unknown_state(msg):
        print "UNNKNOWN - {0}".format(msg)
        sys.exit(3)
