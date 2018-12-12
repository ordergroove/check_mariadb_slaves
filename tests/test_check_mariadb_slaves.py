# -*- coding: utf-8 -*-

import sys
import unittest
import mock

import check_mariadb_slaves


@mock.patch('check_mariadb_slaves.SlaveStatusCheck')
class TestMain(unittest.TestCase):

    def setUp(self):
        self.args = ['--connection', 'connection', '--mode', 'test']

    def test_args_parse_exc(self, mock_SSC):
        mock_SSC.MODES = ('test')

        args = []
        self.assertRaises(SystemExit, check_mariadb_slaves.main, args)

        args = self.args[2:]
        self.assertRaises(SystemExit, check_mariadb_slaves.main, args)

    def test_args_parse(self, mock_SSC):
        mock_SSC.MODES = ('test')
        check_mariadb_slaves.main(self.args)
        mock_SSC.assert_called_once_with('localhost', None, None, 'connection',
                                         'test', False, None, None, False)

        mock_SSC.reset_mock()
        self.args += ['--username', 'test', '--password', 'test', '-w', '10',
                      '-c', '20', '--verbose']
        check_mariadb_slaves.main(self.args)
        mock_SSC.assert_called_once_with('localhost', 'test', 'test',
                                         'connection', 'test', True, 10, 20, False)

        mock_SSC.reset_mock()
        sys.argv = ["myscriptname.py"] + self.args
        check_mariadb_slaves.main()
        mock_SSC.assert_called_once_with('localhost', 'test', 'test',
                                         'connection', 'test', True, 10, 20, False)
