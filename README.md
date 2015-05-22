# check_mariadb_slaves
[![Build Status](https://travis-ci.org/ordergroove/check_mariadb_slaves.svg?branch=master)](https://travis-ci.org/ordergroove/check_mariadb_slaves)

A Nagios plugin written in Python to monitor Maria DB slave metrics. Specifically:
- Replication Lag
- Slave IO running
- Slave SQL running

## Assumptions
- You're familiar with MariaDB
- You're familiar with Nagios
- You're running a MariaDB server that is slaving data

## Requirements
- Python 2.7

## Why?
MariaDB's "multiple master" slaving support is unique and thus, has a slightly different syntax to check on slave status than the traditional "single master" implementation offered by MySQL. MariaDB allows you to check on the status of ALL slave connections or individual slave connections. This plugin leverages the ```SHOW SLAVE ["connection_name"] STATUS``` syntax to check on the slave status(es) of a particular connection. For more information about MariaDB slave status, see https://mariadb.com/kb/en/mariadb/show-slave-status/

Most database metrics you may want to monitor on MariaDB actually parallel MySQL. We use the *check_mysql_health* plugin:
- https://exchange.nagios.org/directory/MySQL/check_mysql_health/details

## Installation
- Get the *check_mariadb_slave.py* script into your Nagios plugins directory (i.e. */usr/local/nagios/libexec*)
- ```chmod u+x check_mariadb_slave.py```

## Command Line Parameters
- --hostname - [*optional*] - hostname of the MariaDB slave
- --username - [*optional*] - user to login to the MariaDB slave as
- --password - [*optional*] - password of said user
- --connection - __[required]__ - the ```"connection_name"``` to use in the ```SHOW SLAVE ["connection_name"] STATUS``` command
- --mode - __[required]__ - the slave status to check. Current available options are 
  - replication_lag
  - slave_io
  - slave_sql
- -w or --warning - warning threshold; currently only required for ```replication_lag``` mode
- -c or --critical - critical threshold; currently only required for ```replication_lag``` mode
- --verbose - [*optional*] - for testing purposes; currently prints out the result of the slave status query when used

## Example Usage
Here's an example of Nagios command and service definitions that implement this plugin:

### commands.cfg
```
define command {
    command_name check_mariadb_slave
    command_line $USER1$/check_mariadb_slave.py --hostname $HOSTADDRESS$ --username $USER3$ --password '$USER4$' --connection $ARG1$ --mode $ARG2$ -w $ARG3$ -c $ARG4$
}
```

### services.cfg
```
define service {    
    use                     generic-service
    hostgroup_name          mariadb_slaves
    service_description     MariaDB SlaveSQL Running - config connection
    check_command           check_mariadb_slave!config!slave_sql!0!0
}   

define service {
    use                     generic-service
    hostgroup_name          mariadb_slaves
    service_description     MariaDB SlaveIO Running - config connection
    check_command           check_mariadb_slave!config!slave_io!0!0
}

define service {
    use                     generic-service
    hostgroup_name          mariadb_slaves
    service_description     MariaDB Replication Lag - config connection
    check_command           check_mariadb_slave!config!replication_lag!125!300
}
```

## Special Thanks to OrderGroove
We would like to take this opportunity to thank everyone at <a href="http://www.ordergroove.com" target="_blank"><img src="http://www.ordergroove.com/sites/all/themes/order_groove/ordergroove_logo.png" width="100"/></a> for allowing us the time to work on open sourcing this project. Without their support, this project would not exist.

License
=======
The MIT License (MIT)

Copyright (c) 2015 OrderGroove

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
