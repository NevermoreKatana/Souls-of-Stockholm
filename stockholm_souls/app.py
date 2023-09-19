import os
import dotenv
from stockholm_souls.database.db import verification, take_user_id, take_user_info
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
    user = {
        'id': f'{id}',
        'name': name,
        'passwd': passwd
    }
    session['user'] = user
    flash('Успешный вход')
    return redirect(f'/profile/{id}')


@app.route('/profile/<id>', methods=['GET'])
def show_profile(id):
    user_info = take_user_info(id)
    return render_template('/user/profile.html', info = user_info)


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