#!/usr/bin/env python
"""MariaDB slave status checker"""
import sys
import argparse
import MySQLdb


class NagiosPlugin(object):

    def ok_state(self, msg):
        print "OK - {}".format(msg)
        sys.exit(0)

    def warning_state(self, msg):
        print "WARNING - {}".format(msg)
        sys.exit(1)

    def critical_state(self, msg):
        print "CRITICAL - {}".format(msg)
        sys.exit(2)

    def unknown_state(self, msg):
        print "UNNKNOWN - {}".format(msg)
        sys.exit(3)


class SlaveStatusCheck(NagiosPlugin):
    """Class to help us run slave status queries against MariaDB"""
    REPLICATION_LAG_MODE = 'replication_lag'
    SLAVESQL_MODE = 'slave_sql'
    SLAVEIO_MODE = 'slave_io'
    MODES = (REPLICATION_LAG_MODE,
             SLAVESQL_MODE,
             SLAVEIO_MODE)

    def __init__(self, hostname, username, password, slave_conn,
                 mode, verbose=False, warning=None, critical=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.warning = warning
        self.critical = critical
        self.verbose = verbose
        self.mode = mode

        # Execute the query and store the results
        self._slave_status = {}
        self.get_slave_status(slave_conn)

    def run_check(self):
        """Execute the check against the given mode"""
        check_fn = getattr(self, self.mode)
        check_fn()

    def replication_lag(self):
        """Check replication lag thresholds"""
        lag = self._slave_status.get('Seconds_Behind_Master')
        if lag is None:
            self.unknown_state("No replication lag reported")

        if not self.warning or not self.critical:
            self.unknown_state("Warning and critical thresholds undefined")

        lag = int(lag)
        warning = int(self.warning)
        critical = int(self.critical)
        lag_msg = "Slave is {0} seconds behinds master".format(lag)

        if lag >= warning and lag < critical:
            self.warning_state(lag_msg)
        elif lag >= critical:
            self.critical_state(lag_msg)

        self.ok_state(lag_msg)

    def slave_sql(self):
        """Check that Slave_SQL_Running = Yes"""
        if self._slave_status.get('Slave_SQL_Running') == "No":
            msg = "Slave sql is not running. Last error: {}".format(
                self._slave_status.get('Last_SQL_Error'))
            self.critical_state(msg)

        self.ok_state("Slave sql is running")

    def slave_io(self):
        """Check that Slave_IO_Running = Yes"""
        if self._slave_status.get('Slave_IO_Running') == "No":
            msg = "Slave io is not running. Last error: {}".format(
                self._slave_status.get('Last_IO_Error'))
            self.critical_state(msg)

        self.ok_state("Slave io is running")

    def get_slave_status(self, slave_connection):
        """Run the query!"""
        try:
            sql = 'SHOW SLAVE "{0}" STATUS'.format(slave_connection)
            conn = None
            conn = MySQLdb.Connection(
                self.hostname,
                self.username,
                self.password)

            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute(sql)
            conn.commit()

            self._slave_status = curs.fetchall()[0]
            if self.verbose:
                print self._slave_status
        except MySQLdb.Error, exc:
            msg = "{0}: {1}".format(exc.args[0], exc.args[1])
            self.unknown_state(msg)
        finally:
            if conn:
                conn.close()


def main():
    """starter method"""
    parser = argparse.ArgumentParser(description='MariaDB slave status checker')
    parser.add_argument('--hostname', default='localhost', type=str,
                        help="MariaDB hostname")
    parser.add_argument('--username', type=str, help="MariaDB username")
    parser.add_argument('--password', type=str, help="MariaDB password")
    parser.add_argument('--connection', required=True, type=str,
                        help="MariaDB slave connection")
    parser.add_argument('--mode', type=str, required=True,
                        choices=SlaveStatusCheck.MODES,
                        help="slave state to check")
    parser.add_argument('-w', '--warning', type=int, default=None,
                        help="warning limit")
    parser.add_argument('-c', '--critical', type=int, default=None,
                        help="critical limit")
    parser.add_argument('--verbose', action='store_true', default=False,
                        help="enable verbose mode")

    args = parser.parse_args()
    ssc = SlaveStatusCheck(args.hostname, args.username, args.password,
                           args.connection, args.mode, args.verbose,
                           args.warning, args.critical)
    ssc.run_check()

if __name__ == '__main__':
    main()
