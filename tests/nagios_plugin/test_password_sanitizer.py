# -*- coding: utf-8 -*-

import unittest

from nagios_plugin.password_sanitizer import sanitize_passwords


class TestSanitizeSetPasswordSyntax(unittest.TestCase):
    TEST_MSG_TPL = """
    CRITICAL - Slave sql is not running. Last error: Error Operation SET PASSWORD
    failed for user@127.0.0.1 on query. Default database: .
    Query: {}
    """

    def _check_sanitize_fn(self, expected_query, test_query):
        expected_msg = self.TEST_MSG_TPL.format(expected_query)
        test_msg = self.TEST_MSG_TPL.format(test_query)
        self.assertEqual(
            expected_msg,
            sanitize_passwords(test_msg)
        )

    def test_sanitizing_the_simplest_set_password_usage(self):
        expected_query = 'SET PASSWORD = ***'
        test_query = 'SET PASSWORD = "hashed value"'
        self._check_sanitize_fn(expected_query, test_query)

    def test_anything_after_an_equal_sign_until_a_closing_set_of_quotes_gets_sanitized(self):
        expected_query = 'SET PASSWORD = ***'
        test_query = 'SET PASSWORD = LOTS OF \'OPERATIONS FOR("password") SETTING\''
        self._check_sanitize_fn(expected_query, test_query)

    def test_anything_before_an_equal_sign_is_preserved(self):
        expected_query = 'SET PASSWORD LOTS OF PREPARING FOR "this": = ***'
        test_query = 'SET PASSWORD LOTS OF PREPARING FOR "this": = AND AFTER OLDPASSWORD("password")'
        self._check_sanitize_fn(expected_query, test_query)
