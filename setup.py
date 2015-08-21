"""Setup file for check_mariadb_slaves module"""
from setuptools import setup, find_packages


setup(
    name='check-mariadb-slaves',
    version='1.1',
    include_package_data=True,
    packages=find_packages(),
    license="MIT",
    author="Juan Gutierrez",
    author_email="juanny.gee@gmail.com",
    description="Nagios Plugin written in Python to monitor MariaDB slave metrics",
    url="https://github.com/ordergroove/check_mariadb_slaves"
)
