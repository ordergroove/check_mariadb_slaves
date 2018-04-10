import mock
import unittest
import check_mariadb_slaves
import MySQLdb
import sys


@mock.patch('check_mariadb_slaves.sys')
class TestNagiosPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin_inst = check_mariadb_slaves.NagiosPlugin(None, None)
        self.msg = "test"

    def test_run_check(self, mock_sys):
        self.assertRaises(NotImplementedError, self.plugin_inst.run_check)

    def test_ok_state(self, mock_sys):
        self.plugin_inst.ok_state(self.msg)
        mock_sys.exit.assert_called_once_with(0)
        mock_sys.stdout.write.called_once_with("OK - {0}".format(self.msg))

    def test_warning_state(self, mock_sys):
        self.plugin_inst.warning_state(self.msg)
        mock_sys.exit.assert_called_once_with(1)
        mock_sys.stdout.write.called_once_with("WARNING - {0}".format(self.msg))

    def test_critical_state(self, mock_sys):
        self.plugin_inst.critical_state(self.msg)
        mock_sys.exit.assert_called_once_with(2)
        mock_sys.stdout.write.called_once_with("CRITICAL - {0}".format(self.msg))

    def test_unknown_state(self, mock_sys):
        self.plugin_inst.unknown_state(self.msg)
        mock_sys.exit.assert_called_once_with(3)
        mock_sys.stdout.write.called_once_with("UNKNOWN - {0}".format(self.msg))


class TestSlaveStatusCheck(unittest.TestCase):

    def setUp(self):
        self.class_args = {
            'hostname': 'test_hostname',
            'username': 'test_username',
            'password': 'test_password',
            'connection_name': 'test_conn',
            'mode': 'test_mode'
        }
        self.slave_status_check = check_mariadb_slaves.SlaveStatusCheck(**self.class_args)

        # Mock the NagiosPlugin methods and how they would behave - i.e. SytemExit is raised
        self.slave_status_check.ok_state = mock.Mock()
        self.slave_status_check.warning_state = mock.Mock(side_effect=SystemExit)
        self.slave_status_check.critical_state = mock.Mock(side_effect=SystemExit)
        self.slave_status_check.unknown_state = mock.Mock(side_effect=SystemExit)

    def test_run_check(self):
        self.assertRaises(AttributeError, self.slave_status_check.run_check)

        self.slave_status_check.replication_lag = mock.Mock()
        self.slave_status_check.mode = self.slave_status_check.REPLICATION_LAG_MODE
        self.slave_status_check.run_check()
        self.slave_status_check.replication_lag.assert_called_once_with()

    def test_replication_lag(self):

        self.assertRaises(SystemExit, self.slave_status_check.replication_lag)
        self.slave_status_check.unknown_state.assert_called_once_with("No replication lag reported")

        self.slave_status_check.unknown_state.reset_mock()
        self.slave_status_check.unknown_state.side_effect = SystemExit
        self.slave_status_check._slave_status["Seconds_Behind_Master"] = 0
        self.assertRaises(SystemExit, self.slave_status_check.replication_lag)
        self.slave_status_check.unknown_state.assert_called_once_with("Warning and critical thresholds undefined")

        lag = 1
        self.slave_status_check.warning = 10
        self.slave_status_check.critical = 100
        self.slave_status_check._slave_status["Seconds_Behind_Master"] = lag
        self.slave_status_check.replication_lag()
        expected_msg = "Slave is {0} seconds behind master | replication_lag={0};10;100".format(lag)
        self.slave_status_check.ok_state.assert_called_once_with(expected_msg)

        lag = 10
        self.slave_status_check._slave_status["Seconds_Behind_Master"] = lag
        self.assertRaises(SystemExit, self.slave_status_check.replication_lag)
        expected_msg = "Slave is {0} seconds behind master | replication_lag={0};10;100".format(lag)
        self.slave_status_check.warning_state.assert_called_once_with(expected_msg)

        lag = 100
        self.slave_status_check._slave_status["Seconds_Behind_Master"] = lag
        self.assertRaises(SystemExit, self.slave_status_check.replication_lag)
        expected_msg = "Slave is {0} seconds behind master | replication_lag={0};10;100".format(lag)
        self.slave_status_check.critical_state.assert_called_once_with(expected_msg)

    def test_slave_sql(self):
        self.slave_status_check._slave_status["Slave_SQL_Running"] = "Yes"
        self.slave_status_check.slave_sql()
        self.slave_status_check.ok_state.assert_called_once_with("Slave sql is running")

        sql_error = "Last error"
        self.slave_status_check._slave_status["Slave_SQL_Running"] = "No"
        self.slave_status_check._slave_status["Last_SQL_Error"] = sql_error

        self.assertRaises(SystemExit, self.slave_status_check.slave_sql)

        expected_msg = "Slave sql is not running. Last error: {0}".format(sql_error)
        self.slave_status_check.critical_state.assert_called_once_with(expected_msg)

    def test_slave_io(self):
        self.slave_status_check._slave_status["Slave_IO_Running"] = "Yes"
        self.slave_status_check.slave_io()
        self.slave_status_check.ok_state.assert_called_once_with("Slave io is running")

        sql_error = "Last error"
        self.slave_status_check._slave_status["Slave_IO_Running"] = "No"
        self.slave_status_check._slave_status["Last_IO_Error"] = sql_error

        self.assertRaises(SystemExit, self.slave_status_check.slave_io)

        expected_msg = "Slave io is not running. Last error: {0}".format(sql_error)
        self.slave_status_check.critical_state.assert_called_once_with(expected_msg)

    @mock.patch('check_mariadb_slaves.MySQLdb.Connection')
    def test_get_slave_status_exc(self, mock_mysqldb_connection):
        mock_mysqldb_connection.side_effect = MySQLdb.Error('test code', 'test exc')
        self.assertRaises(SystemExit, self.slave_status_check.get_slave_status)
        self.slave_status_check.unknown_state.assert_called_once_with('test code: test exc')

    @mock.patch('check_mariadb_slaves.MySQLdb')
    def test_get_slave_status_success(self, mock_mysqldb):
        cursor_ret = [{'foo': 'bar'}]
        cursor_mock = mock_mysqldb.Connection.return_value.cursor
        cursor_mock.return_value.fetchall.return_value = cursor_ret
        self.slave_status_check.get_slave_status()

        self.assertEqual(cursor_ret[0], self.slave_status_check._slave_status)
        mock_mysqldb.Connection.return_value.close.assert_called_once_with()


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
                                         'test', False, None, None)

        mock_SSC.reset_mock()
        self.args += ['--username', 'test', '--password', 'test', '-w', '10',
                      '-c', '20', '--verbose']
        check_mariadb_slaves.main(self.args)
        mock_SSC.assert_called_once_with('localhost', 'test', 'test',
                                         'connection', 'test', True, 10, 20)

        mock_SSC.reset_mock()
        sys.argv = ["myscriptname.py"] + self.args
        check_mariadb_slaves.main()
        mock_SSC.assert_called_once_with('localhost', 'test', 'test',
                                         'connection', 'test', True, 10, 20)
