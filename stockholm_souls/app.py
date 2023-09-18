import os
import dotenv
from flask import Flask, render_template, request, flash, redirect

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
