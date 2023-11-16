from .app import app
from flask import request, jsonify
from .file import get_file


@app.route('/api/v1/file/<short_link>', methods=['GET'])
def file_get_file(short_link):
    file = get_file(short_link)
    if file is None:
        return jsonify({
            'error': 'file not found'
        }), 404
    return jsonify(file), 200

