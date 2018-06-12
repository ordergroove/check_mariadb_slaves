# Version 2.0
* Drop python 2.6 support
* Add python 3.4, 3.5, 3.6 support
  * Replace `MySQLdb` with [`mysqlclient`](https://pypi.org/project/mysqlclient/), a friendly fork of `MySQLdb` with multiversion python support
* Sanitize passwords when found in critical messages
* Package restructuring
