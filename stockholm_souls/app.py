import os
import dotenv
from flask import Flask, render_template, request, flash, redirect, jsonify

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
    return render_template('/user/profile.html')


@app.route('/test', methods=['GET'])
def test():
    return 'INFO'