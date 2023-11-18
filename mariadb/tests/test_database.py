from datetime import datetime
from os import environ
import pymysql
import pytest


options = {
        'host': environ.get('MARIADB_HOST', 'localhost'),
        'port': int(environ.get('MARIADB_PORT', 3306)),
        'user': environ.get('MARIADB_USER'),
        'password': environ.get('MARIADB_PASSWORD'),
        'database': environ.get('MARIADB_DATABASE', 'filefort')
    }


@pytest.fixture
def connection() -> pymysql.connections.Connection:
    with pymysql.connect(**options) as conn:
        yield conn


@pytest.fixture
def cursor(connection) -> pymysql.cursors.Cursor:
    cursor = connection.cursor()
    return cursor


def sample_users(connection, cursor) -> list:
    """
    Guarantee test users are in users table, if not inserts them
    Returns a list of user UUIDs
    """
    sample_data = [
            ('user1', None),
            ('user2', 5),
            ('user3', 100)
            ]
    insert_query = 'INSERT INTO users (name, upload_limit) VALUES (%s, %s)'
    cursor.executemany(insert_query, sample_data)
    cursor.execute('SELECT id FROM users')
    uuids = [t[0] for t in cursor.fetchall()]
    connection.commit()
    return uuids


def empty_db(connection, cursor) -> None:
    cursor.execute('DELETE FROM files')
    cursor.execute('DELETE FROM users')
    connection.commit()


def test_database_connection(connection, cursor):
    assert connection.open


def test_uploader_gets_owner_permissions(connection, cursor):
    empty_db(connection, cursor)
    user_ids = sample_users(connection, cursor)

    files = [(user_ids[i], f'f{i}', f'url{i}', f'mime{i}', '1970-01-01', 'public') for i in range(len(user_ids))]
    query = 'INSERT INTO files(uploader_id, short_link, url, mime_type, expires, privacy) VALUES (%s, %s, %s, %s, %s, %s)'
    cursor.executemany(query, files)

    cursor.execute('SELECT id, uploader_id FROM files')
    file_uploaders = dict(cursor.fetchall())

    cursor.execute('SELECT file_id, user_id FROM permissions WHERE permission = "owner"')
    file_owners = dict(cursor.fetchall())

    assert file_uploaders == file_owners, f"file uploaders were not given file owner permissions"

    connection.rollback()


def test_remove_expired(connection, cursor):
    empty_db(connection, cursor)
    user_ids = sample_users(connection, cursor)

    expired_files = [(user_ids[i], f'f{i}', f'url{i}', f'mime{i}', '1970-01-01', 'public') for i in range(len(user_ids))]
    query = 'INSERT INTO files(uploader_id, short_link, url, mime_type, expires, privacy) VALUES (%s, %s, %s, %s, %s, %s)'

    cursor.executemany(query, expired_files)
    connection.commit()

    cursor.callproc('RemoveExpired', ('2023-11-17', 0))
    # NOTE: kind of hacky, pymysql was not playing nice with output from a stored procedure
    removed_files = cursor.rowcount - 1

    assert len(expired_files) == removed_files, f'number of removed files ({removed_files}) does not match the number of expired files ({len(expired_files)})'
