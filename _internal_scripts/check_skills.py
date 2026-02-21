import pymysql
pymysql.install_as_MySQLdb()
import os
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_py_joinroster_co.settings")
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES LIKE 'skills'")
    row = cursor.fetchone()
    print(f"Table skills exists: {row}")

    if row:
        cursor.execute("DESCRIBE skills")
        columns = cursor.fetchall()
        for col in columns:
            print(col)
