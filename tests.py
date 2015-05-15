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
