# Required library for MySQL: pymysql
# Install via PIP: pip install pymysql
from django.conf import settings

if settings.DB == 'mysql':
    import pymysql

    pymysql.install_as_MySQLdb()
