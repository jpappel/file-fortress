# adapted from https://stackoverflow.com/a/48059894/18579223 
import pymysql
from dbutils.persistent_db import PersistentDB
import os


def _connect_db() -> PersistentDB:
    return PersistentDB(
        creator=pymysql,
        user=os.environ.get('MARIADB_USER'),
        password=os.environ.get('MARIADB_PASSWORD'),
        host="mariadb",
        port=3306,
        database="filefort",
        cursorclass=pymysql.cursors.DictCursor
        )


def get_db() -> PersistentDB:
    return _connect_db()
