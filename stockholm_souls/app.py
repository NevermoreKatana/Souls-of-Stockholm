import os
import dotenv
from stockholm_souls.database.db_posts_handlers import take_all_posts
from stockholm_souls.app_handlers.api_handlers import api_blueprint
from stockholm_souls.app_handlers.user_handlers import users_blueprint
from stockholm_souls.app_handlers.posts_handlers import posts_blueprint
from stockholm_souls.searching import search_posts_by_name
from flask import Flask, render_template, session, request
from flask_jwt_extended import JWTManager

dotenv.load_dotenv()

app = Flask(__name__, static_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_blueprint(api_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)
jwt = JWTManager(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['query']
        posts_data = take_all_posts()
        posts_data = search_posts_by_name(search_query, posts_data)
    elif request.method == 'GET':
        posts_data = take_all_posts()
    current_user = session.get('user')
    if current_user:
        return render_template('index.html', cu = current_user, posts=posts_data)
    return render_template('index.html',posts=posts_data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error/index.html')


@app.route('/docs', methods=['GET'])
def show_docs():
    current_user = session.get('user')
    return render_template('docs.html', cu=current_user)


