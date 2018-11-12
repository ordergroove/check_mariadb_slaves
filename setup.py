"""Setup file for check_mariadb_slaves module"""

from setuptools import setup, find_packages


setup(
    name='check-mariadb-slaves',
    version='2.1',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'mysqlclient==1.3.12'
    ],
    license="MIT",
    author="Juan Gutierrez",
    author_email="juanny.gee@gmail.com",
    description="Nagios Plugin written in Python to monitor MariaDB slave metrics",
    url="https://github.com/ordergroove/check_mariadb_slaves"
)
