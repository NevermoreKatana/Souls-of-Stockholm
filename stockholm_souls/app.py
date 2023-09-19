import os
import dotenv
from stockholm_souls.database.db import take_user_info
from flask import Flask, render_template, request, flash, redirect, jsonify, flash

dotenv.load_dotenv()

app = Flask(__name__, static_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('/user/index.html')


@app.route('/login/', methods=['POST'])
def login_user():
    name = request.form['uname']
    passwd = request.form['passwd']
    info = take_user_info(name, passwd)
    if info:
        flash(info)
        return redirect('/login')
    return 'успех'


@app.route('/test', methods=['GET'])
def test():
    errors = {
        'login': 'asdasd',
        'password': '123',
        'jopa': 'asdasda'
    }
    return errors