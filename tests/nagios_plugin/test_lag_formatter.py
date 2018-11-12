# -*- coding: utf-8 -*-

import unittest

from nagios_plugin.lag_formatter import format_lag


class TestLagFormatter(unittest.TestCase):

    def test_response_contains_all_parts(self):
        self.assertEqual(format_lag(3661), '1 hour 1 minute 1 second')

    def test_response_ignores_empty_parts(self):
        self.assertEqual(format_lag(3601), '1 hour 1 second')
        self.assertEqual(format_lag(61), '1 minute 1 second')
        self.assertEqual(format_lag(3600), '1 hour')

    def test_response_adds_plural_to_formatted_parts(self):
        self.assertEqual(format_lag(7322), '2 hours 2 minutes 2 seconds')
