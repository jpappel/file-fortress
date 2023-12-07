from flask import Blueprint, request, current_app, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

users = Blueprint('users', __name__)


class User(UserMixin):
    pass


user_accounts = {'demo': 'password'}
login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def user_loader(username):
    if username not in user_accounts:
        return

    user = User()
    user.id = username
    return user


@users.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            return render_template('login.html')
        case 'POST':
            username = request.form['username']
            password = request.form['password']
            if username in user_accounts and password == user_accounts[username]:
                user = User()
                user.id = username
                login_user(user)
                return redirect(url_for('users.upload'))
            return 'Bad Login'


@users.route('/upload', methods=['GET'])
@login_required
def upload():
    return render_template('upload.html')


@users.route('/logout')
@login_required
def logout():
    logout_user
    return 'Logged out'
