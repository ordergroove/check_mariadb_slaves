# -*- coding: utf-8 -*-

import unittest

from nagios_plugin.password_sanitizer import sanitize_passwords


class TestSanitizePasswordsTestCase(unittest.TestCase):
    TEST_MSG_TPL = ''

    def _check_sanitize_fn(self, expected_query, test_query):
        expected_msg = self.TEST_MSG_TPL.format(expected_query)
        test_msg = self.TEST_MSG_TPL.format(test_query)
        self.assertEqual(
            expected_msg,
            sanitize_passwords(test_msg)
        )


class TestSanitizeSetPasswordSyntax(TestSanitizePasswordsTestCase):
    TEST_MSG_TPL = """
    CRITICAL - Slave sql is not running. Last error: Error Operation SET PASSWORD
    failed for user@127.0.0.1 on query. Default database: .
    Query: {}
    """

    def test_anything_after_an_equal_sign_until_a_closing_set_of_quotes_gets_sanitized(self):
        expected_query = 'SET PASSWORD = ***'
        test_query = 'SET PASSWORD = LOTS OF \'OPERATIONS FOR("password") SETTING\''
        self._check_sanitize_fn(expected_query, test_query)

    def test_anything_before_an_equal_sign_is_preserved(self):
        expected_query = 'SET PASSWORD LOTS OF PREPARING FOR "this": = ***'
        test_query = 'SET PASSWORD LOTS OF PREPARING FOR "this": = AND AFTER OLDPASSWORD("password")'
        self._check_sanitize_fn(expected_query, test_query)


class TestSanitizeUserIdentifiedSyntax(TestSanitizePasswordsTestCase):
    TEST_MSG_TPL = """
    CRITICAL - Slave sql is not running. Last error: Error Operation ALTER USER
    failed for user@127.0.0.1 on query. Default database: .
    Query: {}
    """

    def test_alter_user_password_query_using_IDENTIFIED_BY_syntax_gets_sanitized(self):
        expected_query = "ALTER USER foo IDENTIFIED BY ***;"
        test_query = "ALTER USER foo IDENTIFIED BY 'something';"
        self._check_sanitize_fn(expected_query, test_query)

    def test_alter_user_password_query_using_IDENTIFIED_BY_PASSWORD_syntax_gets_sanitized(self):
        expected_query = "ALTER USER foo IDENTIFIED BY ***;"
        test_query = "ALTER USER foo IDENTIFIED BY PASSWORD 'something';"
        self._check_sanitize_fn(expected_query, test_query)

    def test_create_user_query_with_auth_plugin_and_password_using_AS_syntax_gets_sanitized(self):
        expected_query = "CREATE USER foo IDENTIFIED WITH authentication_plugin AS ***"
        test_query = "CREATE USER foo IDENTIFIED WITH authentication_plugin AS 'hash_string'"
        self._check_sanitize_fn(expected_query, test_query)

    def test_create_user_query_with_auth_plugin_and_password_using_USING_syntax_gets_sanitized(self):
        expected_query = "CREATE USER foo IDENTIFIED WITH authentication_plugin USING ***"
        test_query = "CREATE USER foo IDENTIFIED WITH authentication_plugin USING 'hash_string'"
        self._check_sanitize_fn(expected_query, test_query)

    def test_create_user_query_with_auth_plugin_and_no_password_is_unaltered(self):
        test_query = "CREATE USER foo IDENTIFIED VIA authentication_plugin"
        self._check_sanitize_fn(test_query, test_query)
