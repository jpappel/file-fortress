# adapted from https://stackoverflow.com/a/48059894/18579223 
import pymysql
from flask import Flask, g, request
from dbutils.persistent_db import PersistentDB
from app import app
import os

def _connect_db():
    return PersistentDB(
        creator=pymysql,
        user=os.environ.get('MARIADB_USER'),
        password=os.environ.get('MARIADB_PASSWORD'),
        host="mariadb",
        port=3306,
        database="filefort",
        cursorclass=pymysql.cursors.DictCursor
        )
def get_db():
    if not hasattr(app, 'db'):
        app.db = _connect_db()
    return app.db.connection()

    


