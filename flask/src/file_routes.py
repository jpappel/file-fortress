from .app import app
from flask import request, jsonify, send_file, make_response
from .util import get_mime_type

from .StorageManagers import LocalStorageManager
from .db import get_db


@app.route('/api/v1/file/<short_link>', methods=['GET', 'DELETE'],
           provide_automatic_options=False)
def file(short_link):
    # TODO: add manager as app attribute
    manager = LocalStorageManager(get_db(), '/mnt/file_storage')
    try:
        rel_path = manager.lookup_link(short_link)
    except FileNotFoundError:
        return jsonify({'error': 'file not found'}), 404

    match request.method:
        case 'GET':
            path = manager.cannonical_location(rel_path)
            return send_file(path)
        case 'DELETE':
            manager.delete_file(rel_path)
            cursor = get_db().cursor()
            cursor.execute('DELETE FROM files WHERE short_link = %s', short_link)
            get_db().commit()
            return {}, 204

@app.route('/api/v1/file', methods=['POST'], provide_automatic_options=False)
@app.route('/api/v1/file/<short_link>', methods=['POST'],
           provide_automatic_options=False)
def upload_file(short_link:str=None):


    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400

    # NOTE: any form is required to have
    # <input type="file" name="file"></input>
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'empty file provided'}), 400
    
    manager = LocalStorageManager(get_db(), '/mnt/file_storage')
    if short_link is None:
        short_link = manager.generate_short_link()

    filename = file.filename
    file_info = {
            'short_link': short_link,
            'mime_type': get_mime_type(file.read(3072)),
            'privacy': request.args.get('privacy', 'public'),
            }

    # reset to beginning of file
    file.seek(0)


    # TODO: change from testing value of system user id
    file_info['uploader_id'] = manager._system_id

    try:
        file_info['expires'] = int(request.args.get('expires'))
    except (ValueError, TypeError):
        file_info['expires'] = None

    file_info['url'] = manager.allocate_url(file_info['uploader_id'], filename)

    # create link within database
    manager.create_link(**file_info)

    # save file
    manager.push_file(file.stream, file_info['url'])

    return jsonify({'success': 'file uploaded succesfully'}), 200


@app.route('/api/v1/file/<short_link>', methods=['OPTIONS'],
           provide_automatic_options=False)
def link_options(short_link):
    allowed_methods = ['HEAD', 'OPTIONS']

    # query database for short_link
    cursor = get_db().cursor()
    cursor.execute('SELECT id FROM files WHERE short_link = %s', short_link)
    result = cursor.fetchone()

    # find valid methods
    if result is None:
        allowed_methods.append('POST')
    else:
        allowed_methods.append('GET')
        allowed_methods.append('DELETE')

    response = make_response()
    response.headers['Allow'] = ', '.join(allowed_methods)
    return response, 204


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
