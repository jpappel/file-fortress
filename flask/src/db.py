# adapted from https://stackoverflow.com/a/48059894/18579223 
import pymysql
from dbutils.persistent_db import PersistentDB
import os


def _connect_db(creator=pymysql, user=None, password=None, host='mariadb',
                port=3306, database='filefort',
                cursorclass=pymysql.cursors.DictCursor) -> PersistentDB:
    return PersistentDB(
        creator=creator,
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        cursorclass=cursorclass
        )


def get_db() -> PersistentDB:
    return _connect_db(user=os.environ.get('MARIADB_USER'),
                       password=os.environ.get('MARIADB_PASSWORD'))
