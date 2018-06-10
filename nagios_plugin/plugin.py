# -*- coding: utf-8 -*-
"""MariaDB slave status checker"""

__all__ = ['SlaveStatusCheck']

import MySQLdb
from .base import NagiosPlugin


class SlaveStatusCheck(NagiosPlugin):
    """Class to help us run slave status queries against MariaDB"""
    REPLICATION_LAG_MODE = 'replication_lag'
    SLAVESQL_MODE = 'slave_sql'
    SLAVEIO_MODE = 'slave_io'
    MODES = (REPLICATION_LAG_MODE,
             SLAVESQL_MODE,
             SLAVEIO_MODE)

    def __init__(self, hostname, username, password, connection_name,
                 mode, verbose=False, warning=None, critical=None):
        super(SlaveStatusCheck, self).__init__(warning, critical)

        self.hostname = hostname
        self.username = username
        self.password = password
        self.connection_name = connection_name
        self.verbose = verbose
        self.mode = mode
        self._slave_status = {}

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
            msg = "Slave sql is not running. Last error: {0}".format(
                self._slave_status.get('Last_SQL_Error'))
            self.critical_state(msg)

        self.ok_state("Slave sql is running")

    def slave_io(self):
        """Check that Slave_IO_Running = Yes"""
        if self._slave_status.get('Slave_IO_Running') == "No":
            msg = "Slave io is not running. Last error: {0}".format(
                self._slave_status.get('Last_IO_Error'))
            self.critical_state(msg)

        self.ok_state("Slave io is running")

    def get_slave_status(self):
        """Run the query!"""
        try:
            sql = 'SHOW SLAVE "{0}" STATUS'.format(self.connection_name)
            conn = None
            conn = MySQLdb.Connection(
                self.hostname,
                self.username,
                self.password)

            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute(sql)
            conn.commit()

            self._slave_status = curs.fetchall()[0]
            if self.verbose: # pragma: no cover
                print(self._slave_status)
        except MySQLdb.Error as exc:
            msg = "{0}: {1}".format(exc.args[0], exc.args[1])
            self.unknown_state(msg)
        finally:
            if conn:
                conn.close()
