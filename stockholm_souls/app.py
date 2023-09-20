import os
import dotenv
from stockholm_souls.database.db import verification, take_user_id, take_user_info, take_additional_user_info,create_new_user, create_session_data, check_user, check_valid_api_key
from stockholm_souls.database.validator import password_checker
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
    errors = password_checker(passwd, confirm_passwd)
    if check_user(name):
        flash({'exist':'A user with this name exists'})
        return redirect('/register')
    elif errors:
        flash(errors)
        return redirect('/register')
    create_new_user(name, passwd, country,gender,age)
    id = take_user_id(name)
    user_data = create_session_data(id)
    session['user'] = user_data
    return redirect(f'/profile/{id}')

@app.route('/profile/<id>', methods=['GET'])
def show_profile(id):
    current_user = session.get('user')
    user_info = take_user_info(id)
    additional_info = take_additional_user_info(id)
    return render_template('/user/profile.html', info = user_info, a_inf=additional_info, cu = current_user)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')



@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    key = data['API_Key']
    user_id = data['user_id']
    check = check_valid_api_key(key, user_id)
    return check
