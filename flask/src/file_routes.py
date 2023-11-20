from .app import app
from flask import request, jsonify, send_file

from .StorageManagers import LocalStorageManager
from .db import get_db


@app.route('/api/v1/file/<short_link>', methods=['GET', 'DELETE', 'PUT'])
def file(short_link):
    print(request.method)
    manager = LocalStorageManager(get_db(), '/mnt/file_storage')
    try:
        rel_path = manager.create_link(short_link) if request.method == 'PUT' else manager.lookup_link(short_link)
    except FileNotFoundError:
        return jsonify({'error': 'file not found'}), 404
    except FileExistsError:
        return jsonify({'error': 'a file already exits at this location'}), 404

    match request.method:
        case 'GET':
            path = manager.cannonical_location(rel_path)
            return send_file(path)
        case 'DELETE':
            manager.delete_file(short_link)
            cursor = get_db().cursor()
            cursor.execute('DROP FROM files WHERE short_link = %s', short_link)
            cursor.commit()
        case 'PUT':
            raise NotImplementedError


@app.route('/api/v1/file/<short_link>/info', methods=['GET'])
def file_info(short_link):
    try:
        cursor = get_db().cursor()
        query = """SELECT files.id AS file_id, name AS uploader_username, mime_type, expires, privacy, modified_date, created_date
        FROM files
        INNER JOIN users
        ON users.id = files.uploader_id
        WHERE short_link=%s
        """
        cursor.execute(query, short_link)
        result = cursor.fetchone()
        if result is None:
            raise FileNotFoundError
        result['modified_date'] = result['modified_date'].timestamp()
        result['created_date'] = result['created_date'].timestamp()
        return jsonify(result), 200
    except FileNotFoundError:
        return jsonify({'error': 'file not found'}), 404
