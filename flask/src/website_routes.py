from flask import Blueprint, render_template

website = Blueprint('website', __name__)


@website.route('/', methods=['GET'])
def web_root():
    return render_template('index.html')


@website.route('/u/<username>', methods=['GET'])
def web_get_user(username):
    return render_template('user.html', username=username)


@website.route('/<short_link>', methods=['GET'])
def web_get_file(short_link):
    return render_template('file.html', short_link=short_link)
