# adapted from https://stackoverflow.com/a/48059894/18579223 
import pymysql
from dbutils.persistent_db import PersistentDB
from .app import app
import os
import time

def _connect_db():
    connected = False
    timeout = 0.5
    # while not connected:
    while True:
        try:
            db = PersistentDB(
                creator=pymysql,
                user=os.environ.get('MARIADB_USER'),
                password=os.environ.get('MARIADB_PASSWORD'),
                host="mariadb",
                port=3306,
                database="filefort",
                cursorclass=pymysql.cursors.DictCursor
                )
            db.connection()
            break
            
        except Exception as e:
            # will wait 63 seconds at most before raising TimeoutError
            timeout = timeout * 2
            if timeout > 32:
                raise TimeoutError("Database connection timeout")
            print(f"Error connecting to MariaDB Platform: {e}, retrying in {int(timeout)} second(s)")
            time.sleep(timeout)
    return db

def get_db():
    if not hasattr(app, 'db'):
        app.db = _connect_db()
    return app.db.connection()

get_db()  


