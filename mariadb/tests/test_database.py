import os
import pymysql
import pytest


options = {
        'host': os.environ.get('MARIADB_HOST', 'localhost'),
        'port': int(os.environ.get('MARIADB_PORT', 3306)),
        'user': os.environ.get('MARIADB_USER'),
        'password': os.environ.get('MARIADB_PASSWORD'),
        'database': os.environ.get('MARIADB_DATABASE', 'filefort')
    }


@pytest.fixture
def connection() -> pymysql.connections.Connection:
    with pymysql.connect(**options) as conn:
        yield conn


@pytest.fixture
def cursor(connection) -> pymysql.cursors.Cursor:
    cursor = connection.cursor()
    return cursor


def sample_users(connection, cursor) -> None:
    """
    Guarantee test users are in users table, if not inserts them
    Returns if users had to be added
    """
    sample_data = [
            ('user1', None),
            ('user2', 5),
            ('user3', 100)
            ]
    insert_query = 'INSERT INTO users (name, upload_limit) VALUES (%s, %s)'
    cursor.executemany(insert_query, sample_data)
    connection.commit()


def empty_db(connection, cursor) -> None:
    cursor.execute('DELETE FROM files')
    cursor.execute('DELETE FROM users')
    connection.commit()


def test_database_connection(connection, cursor):
    assert connection.open


# def test_uploader_gets_owner_permissions(connection, cursor):
#     empty_db(connection, cursor)
#     sample_users(connection, cursor)
#
#     # view = """
#     # CREATE VIEW file_owners AS
#     # SELECT id, short_link, url FROM
#     # files INNER JOIN
#     # permissions
#     # ON files.id = permissions.file_id
#     # """
#
#     cursor.execute('SELECT * FROM permissions WHERE permission = "owner"')
#     file_owners = cursor.fetchall()
#     print(file_owners)
#     # cursor.execute('SELECT * FROM file_owners')
#     cursor.commit()
