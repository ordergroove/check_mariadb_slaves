import mock
import unittest
import check_mariadb_slaves


@mock.patch('check_mariadb_slaves.sys')
class TestNagiosPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin_inst = check_mariadb_slaves.NagiosPlugin()
        self.msg = "test"

    def test_run_check(self, mock_sys):
        with self.assertRaises(NotImplementedError):
            self.plugin_inst.run_check()

    def test_ok_state(self, mock_sys):
        self.plugin_inst.ok_state(self.msg)
        mock_sys.exit.assert_called_once_with(0)
        mock_sys.stdout.write.called_once_with("OK - {}".format(self.msg))

    def test_warning_state(self, mock_sys):
        self.plugin_inst.warning_state(self.msg)
        mock_sys.exit.assert_called_once_with(1)
        mock_sys.stdout.write.called_once_with("WARNING - {}".format(self.msg))

    def test_critical_state(self, mock_sys):
        self.plugin_inst.critical_state(self.msg)
        mock_sys.exit.assert_called_once_with(2)
        mock_sys.stdout.write.called_once_with("CRITICAL - {}".format(self.msg))

    def test_unknown_state(self, mock_sys):
        self.plugin_inst.unknown_state(self.msg)
        mock_sys.exit.assert_called_once_with(3)
        mock_sys.stdout.write.called_once_with("UNKNOWN - {}".format(self.msg))


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

        # Mock the NagiosPlugin methods
        self.slave_status_check.ok_state = mock.Mock()
        self.slave_status_check.warning_state = mock.Mock()
        self.slave_status_check.critical_state = mock.Mock()
        self.slave_status_check.unknown_state = mock.Mock()

    def test_run_check(self):
        with self.assertRaises(AttributeError):
            self.slave_status_check.run_check()

        self.slave_status_check.replication_lag = mock.Mock()
        self.slave_status_check.mode = self.slave_status_check.REPLICATION_LAG_MODE
        self.slave_status_check.run_check()
        self.slave_status_check.replication_lag.assert_called_once_with()

    def test_slave_sql(self):
        self.slave_status_check._slave_status["Slave_SQL_Running"] = "Yes"
        self.slave_status_check.slave_sql()
        self.slave_status_check.ok_state.assert_called_once_with("Slave sql is running")

        sql_error = "Last error"
        self.slave_status_check._slave_status["Slave_SQL_Running"] = "No"
        self.slave_status_check._slave_status["Last_SQL_Error"] = sql_error
        self.slave_status_check.slave_sql()

        expected_msg = "Slave sql is not running. Last error: {}".format(sql_error)
        self.slave_status_check.critical_state.assert_called_once_with(expected_msg)

    def test_slave_io(self):
        self.slave_status_check._slave_status["Slave_IO_Running"] = "Yes"
        self.slave_status_check.slave_io()
        self.slave_status_check.ok_state.assert_called_once_with("Slave io is running")

        sql_error = "Last error"
        self.slave_status_check._slave_status["Slave_IO_Running"] = "No"
        self.slave_status_check._slave_status["Last_IO_Error"] = sql_error
        self.slave_status_check.slave_io()

        expected_msg = "Slave io is not running. Last error: {}".format(sql_error)
        self.slave_status_check.critical_state.assert_called_once_with(expected_msg)
