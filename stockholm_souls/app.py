import os
import dotenv
from stockholm_souls.database.db import verification, take_user_id, take_user_info, take_additional_user_info,create_new_user, create_session_data, check_user
from stockholm_souls.database.validator import password_similarity
from flask import Flask, render_template, request, flash, redirect, jsonify, flash, session

dotenv.load_dotenv()

app = Flask(__name__, static_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    current_user = session.get('user')
    if current_user:
        return render_template('index.html', cu = current_user)
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('/user/index.html')


@app.route('/login/', methods=['POST'])
def login_user():
    name = request.form['uname']
    passwd = request.form['passwd']
    errors = verification(name, passwd)
    if errors:
        flash(errors)
        return redirect('/login')
    id = take_user_id(name)
    user_data = create_session_data(id)
    session['user'] = user_data
    flash('Успешный вход')
    return redirect(f'/profile/{id}')

@app.route('/register', methods=['GET'])
def reg_form():
    return render_template('/user/register.html')


@app.route('/register/', methods=['POST'])
def register_user():
    name = request.form['uname']
    passwd = request.form['passwd']
    confirm_passwd = request.form['confirm_passwd']
    country = request.form['country']
    gender = request.form['gender']
    age = request.form['age']
    errors = password_similarity(passwd, confirm_passwd)
    if errors:
        return redirect('/register')
    if check_user(name):
        flash('User est uje')
        return redirect('/register')
    create_new_user(name, passwd, country,gender,age)
    id = take_user_id(name)
    user_data = create_session_data(id)
    session['user'] = user_data
    return redirect(f'/profile/{id}')

@app.route('/profile/<id>', methods=['GET'])
def show_profile(id):
    user_info = take_user_info(id)
    additional_info = take_additional_user_info(id)
    return render_template('/user/profile.html', info = user_info, a_inf=additional_info)


@app.route('/test', methods=['GET'])
def test():
    errors = {
        'login': 'asdasd',
        'password': '123',
        'jopa': 'asdasda'
    }
    return errors



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')



@app.route('/api/login', methods=['POST'])
def login():
    api_key = request.headers.get('API-Key')
    # username = data.get('username')
    # password = data.get('password')
    return f'{api_key}'