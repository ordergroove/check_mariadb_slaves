"""Setup file for check_mariadb_slaves module"""
from setuptools import setup, find_packages


setup(
    name='check-mariadb-slaves',
    version='1.0',
    include_package_data=True,
    packages=find_packages(),
    license="MIT",
    author="Juan Gutierrez",
    description="Nagios Plugin written in Python to monitor MariaDB slave metrics",
    url="https://github.com/ordergroove/check_mariadb_slaves"
)
