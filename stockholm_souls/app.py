import os
import dotenv
from stockholm_souls.database.validator import password_checker
from stockholm_souls.database.db import (take_all_posts,
                                         take_one_post,
                                         take_comments,
                                         add_comments,
                                         add_new_post,
                                         take_jwt,
                                         )
from stockholm_souls.api_handlers import api_blueprint
from stockholm_souls.user_handlers import users_blueprint
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   jsonify,
                   flash,
                   session)
from flask_jwt_extended import (JWTManager)
dotenv.load_dotenv()

app = Flask(__name__, static_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_blueprint(api_blueprint)
app.register_blueprint(users_blueprint)
jwt = JWTManager(app)



@app.route('/', methods=['GET'])
def index():
    posts_data = take_all_posts()
    current_user = session.get('user')
    if current_user:
        return render_template('index.html', cu = current_user, posts=posts_data)
    return render_template('index.html',posts=posts_data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error/index.html')

@app.route('/post/<id>', methods=['GET'])
def show_post(id):
    post_info = take_one_post(id)
    comments_data = take_comments(id)
    current_user = session.get('user')
    if post_info:
        return render_template('posts/post.html', post=post_info[0], cu=current_user, comments = comments_data)
    return render_template('/error/index.html')


@app.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    content = request.form['comment']
    user = session.get('user')
    if user:
        add_comments(post_id, content, user)
        return redirect(f'/post/{post_id}')
    flash('Войдите в аккаунт')
    return redirect(f'/post/{post_id}')


@app.route('/post/create', methods=['GET'])
def create_post_form():
    current_user = session.get('user')
    return render_template('posts/create_post.html', cu=current_user)

@app.route('/post/create/', methods=['POST'])
def create_post():
    current_user = session.get('user')
    if current_user:
        post_name = request.form['name']
        contet = request.form['content']
        user_id = current_user['id']
        user_name = current_user['name']
        add_new_post(user_id, user_name,post_name,contet)
        return redirect('/')
    flash('Сначала войдите в аккаунт')
    return redirect('/post/create')


@app.route('/docs', methods=['GET'])
def show_docs():
    current_user = session.get('user')
    return render_template('docs.html', cu=current_user)


