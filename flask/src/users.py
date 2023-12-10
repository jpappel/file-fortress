from flask import Blueprint, request, current_app, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash

users = Blueprint('users', __name__)


class User(UserMixin):
    def __init__(self, user_id, name, username, password_hash, salt):
        self.id = user_id
        self.name = name
        self.username = username
        self.password_hash = password_hash
        self.salt = salt


login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def user_loader(username):
    with current_app.config['DB'].connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT id AS user_id, name, username, hash AS password_hash, salt FROM users
        WHERE username = %s
        ''', username)
        user_info = cursor.fetchone()
    return User(**user_info) if user_info else None

@users.route('/register', methods=['GET', 'POST'])
def register():
    match request.method:
        case 'GET':
            return render_template('register.html')

        case 'POST':
            name = request.form.get('name')
            username = request.form['username']
            password = request.form['password']
            # TODO: check if password is secure
            salt = gen_salt(32)
            password_hash = generate_password_hash(password + salt)

            user_info = (name if name is not None else username,
                         username,
                         password_hash,
                         salt)

            with current_app.config['DB'].connection() as conn:
                conn.begin()
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                    INSERT INTO users (name, username, hash, salt)
                    VALUES (%s, %s, %s, %s)
                    ''', user_info)
                    conn.commit()
                    return redirect(url_for('users.login'))
                except Exception:
                    conn.rollback()
                    # # TODO: reload page, prompt about invalid

                return render_template('register.html')



@users.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            return render_template('login.html')
        case 'POST':
            username = request.form['username']
            password = request.form['password']

            with current_app.config['DB'].connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT id AS user_id, name, username, hash AS password_hash, salt FROM users
                WHERE username = %s
                ''', username)
                user_info = cursor.fetchone()

            if user_info and check_password_hash(
                    user_info['password_hash'], password + user_info['salt']):
                user = User(**user_info)
                login_user(user)
                return render_template('upload.html')

            return 'Bad Login'


@users.route('/upload', methods=['GET'])
@login_required
def upload():
    return render_template('upload.html')


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'
