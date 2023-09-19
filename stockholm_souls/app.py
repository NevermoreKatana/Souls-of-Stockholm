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
def log_in():
    return render_template('/user/index.html')


@app.route('/test', methods=['GET'])
def l():
    return jsonify('jopa')